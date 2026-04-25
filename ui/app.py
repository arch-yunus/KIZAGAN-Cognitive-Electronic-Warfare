import csv
import io
import sqlite3
from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO
import threading
import time
from core.orchestrator import SystemOrchestrator
from core.config import UI_HOST, UI_PORT, UPDATE_INTERVAL_MS

import subprocess
import os
import signal

app          = Flask(__name__)
socketio     = SocketIO(app, cors_allowed_origins="*")
orchestrator = SystemOrchestrator()

# --- Simulation Management ---
sim_proc = None

def start_external_simulator():
    global sim_proc
    if sim_proc and sim_proc.poll() is None:
        return # Already running
    
    env_path = os.getcwd()
    # Use the same python executable and set PYTHONPATH
    my_env = os.environ.copy()
    my_env["PYTHONPATH"] = env_path + os.pathsep + my_env.get("PYTHONPATH", "")
    
    script_path = os.path.join(env_path, "sim", "external_signals_source.py")
    try:
        sim_proc = subprocess.Popen(
            [sys.executable, script_path],
            env=my_env,
            creationflags=getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 512) if os.name == 'nt' else 0
        )
    except Exception as e:
        print(f"[!] Simülatör başlatma hatası: {e}")

def stop_external_simulator():
    global sim_proc
    if sim_proc:
        if os.name == 'nt':
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(sim_proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            sim_proc.terminate()
        sim_proc = None

import sys


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/export_report')
def export_report():
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Timestamp', 'Freq_Idx', 'Freq_MHz', 'SNR', 'Type',
                 'Confidence', 'Threat', 'AoA', 'DF_Confidence',
                 'Track_ID', 'Track_Hits', 'RFI_Hash'])
    try:
        with sqlite3.connect("logs/mission_log.db") as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, timestamp, freq_idx, freq_mhz, snr, type, confidence, "
                "threat_level, aoa, df_confidence, track_id, track_hits, rfi_hash "
                "FROM signals ORDER BY timestamp DESC"
            )
            cw.writerows(c.fetchall())
    except Exception as e:
        cw.writerow(["Error", str(e)])
    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=aar_mission_report.csv"},
    )


@app.route('/api/stats')
def get_stats():
    r = orchestrator.latest_results
    if not r:
        return jsonify({})
    try:
        ea = r.get('ea_status') or {}
        ss = r.get('spectrum_stats') or {}
        return jsonify({
            "target_count":   ea.get('target_count', 0),
            "total_reward":   ea.get('reward', 0),
            "epsilon":        ea.get('epsilon', 1.0),
            "episode":        ea.get('episode', 0),
            "q_states":       ea.get('q_states', 0),
            "occupancy_pct":  ss.get('occupancy_pct', 0),
            "peak_pwr_dbm":   ss.get('peak_pwr_dbm', -100),
            "active_sigs":    ss.get('active_sigs', 0),
            "current_action": ea.get('action', 'STANDBY'),
            "rf_source":      ss.get('rf_source', 'LOCAL'),
            "denoiser_on":    ss.get('denoiser_on', True),
        })
    except Exception as e:
        return jsonify({"error": "Internal Error", "details": str(e)}), 500


@app.route('/api/history')
def get_history():
    return jsonify(orchestrator.logger.get_recent_signals(50))


@app.route('/api/threats')
def get_threats():
    return jsonify({
        "threat_stats": orchestrator.logger.get_threat_stats(300),
        "type_stats":   orchestrator.logger.get_type_stats(300),
        "actions":      orchestrator.logger.get_action_history(20),
    })


# ── HIL Telemetry API v1 (New V7) ──────────────────────────────────────────
@app.route('/api/v1/telemetry')
def get_v1_telemetry():
    """HIL-Ready REST endpoint for external mission controllers."""
    r = orchestrator.latest_results
    if not r:
        return jsonify({"status": "unavailable"}), 503
    
    try:
        sigs = r.get("signals")
        if not isinstance(sigs, list): sigs = []
        
        return jsonify({
            "version": "6.0.0", # System core version
            "timestamp": r.get("timestamp"),
            "swarm": orchestrator.friendly_nodes,
            "intel": {
                "signals": [
                    {k: v for k, v in s.items() if k not in ["waterfall_slice"]} 
                    for s in sigs if isinstance(s, dict)
                ],
                "stats": r.get("spectrum_stats")
            },
            "action": r.get("ea_status")
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ── Socket events ─────────────────────────────────────────────────────────────
@socketio.on('set_mode')
def handle_set_mode(data):
    orchestrator.mode = data.get('mode', 'AUTO')


@socketio.on('set_manual_jam')
def handle_manual_jam(data):
    if orchestrator.mode == 'MANUAL':
        orchestrator.manual_jam = data.get('is_jamming', False)


@socketio.on('set_noise_floor')
def handle_noise_floor(data):
    orchestrator.env.noise_floor = float(data.get('noise', -100))


@socketio.on('set_denoiser')
def handle_denoiser(data):
    orchestrator.denoiser_on = bool(data.get('enabled', True))


@socketio.on('control_sim')
def handle_sim_control(data):
    cmd = data.get('command')
    if cmd == 'START':
        start_external_simulator()
    elif cmd == 'STOP':
        stop_external_simulator()
    elif cmd == 'RESTART':
        stop_external_simulator()
        time.sleep(0.5)
        start_external_simulator()


# ── Background emitter ────────────────────────────────────────────────────────
from modules.ai_specialist.explainability import AIExplainer
from sim.ai_adversary import AIAdversary

explainer = AIExplainer()
adversary = AIAdversary()

def background_thread():
    while True:
        # Simulate AI Adversary
        jamming_status = orchestrator.latest_results.get("ea_status", {})
        jam_action = jamming_status.get("action", "STANDBY")
        
        is_jammed = adversary.detect_jamming(jam_action)
        adversary.act(is_jammed)
        
        # Inject adversary signal into environment
        if not hasattr(orchestrator.env, 'active_signals') or orchestrator.env.active_signals is None:
            orchestrator.env.active_signals = []
            
        adv_sig = adversary.get_signal_params()
        # Clean old adversary signals to avoid duplication
        orchestrator.env.active_signals = [s for s in orchestrator.env.active_signals if not s.get('is_adversary')]
        orchestrator.env.active_signals.append(adv_sig)
        
        results = orchestrator.run_cycle()
        
        # Add AI Explainability messages
        results["ai_explanation"] = {
            "dqn": explainer.explain_dqn(jamming_status),
            "adversary": explainer.explain_adversary(adversary.state, adversary.integrity)
        }
        
        socketio.emit('new_spectrum_data', results)
        time.sleep(UPDATE_INTERVAL_MS / 1000.0)


if __name__ == '__main__':
    t = threading.Thread(target=background_thread, daemon=True)
    t.start()
    print(f"Otonom-EH Dashboard: http://localhost:{UI_PORT}")
    socketio.run(app, host=UI_HOST, port=UI_PORT, debug=False)
