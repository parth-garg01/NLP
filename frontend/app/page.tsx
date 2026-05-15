"use client";

import { useEffect, useMemo, useState } from "react";
import { API, fetchJSON } from "../lib/api";

type ModelInfo = { stt_models: string[]; tts_models: string[] };
type HistoryRecord = {
  id: number;
  kind: string;
  output_path: string | null;
  transcript: string | null;
  confidence: number | null;
  voice: string | null;
  created_at: string;
};

export default function Page() {
  const [models, setModels] = useState<ModelInfo | null>(null);
  const [health, setHealth] = useState("checking...");
  const [history, setHistory] = useState<HistoryRecord[]>([]);
  const [sttFile, setSttFile] = useState<File | null>(null);
  const [sttResult, setSttResult] = useState("");
  const [ttsText, setTtsText] = useState("Hello from VoxCraft.");
  const [ttsVoice, setTtsVoice] = useState("tts_models/en/ljspeech/tacotron2-DDC");
  const [ttsResult, setTtsResult] = useState("");

  const topHistory = useMemo(() => history.slice(0, 8), [history]);

  async function loadBootData() {
    try {
      const [m, h, hist] = await Promise.all([
        fetchJSON<ModelInfo>("/api/models"),
        fetchJSON<{ status: string }>("/api/health"),
        fetchJSON<HistoryRecord[]>("/api/history"),
      ]);
      setModels(m);
      setHealth(h.status);
      setHistory(hist);
      if (m.tts_models.length) setTtsVoice(m.tts_models[0]);
    } catch (e) {
      setHealth("down");
    }
  }

  useEffect(() => {
    loadBootData();
  }, []);

  async function runSTT() {
    if (!sttFile) return;
    const form = new FormData();
    form.append("file", sttFile);
    form.append("export_format", "txt");

    const res = await fetch(`${API}/api/stt`, { method: "POST", body: form });
    const data = await res.json();
    setSttResult(JSON.stringify(data, null, 2));
    await loadBootData();
  }

  async function runTTS() {
    const form = new FormData();
    form.append("text", ttsText);
    form.append("voice", ttsVoice);
    form.append("rate", "1");
    form.append("pitch", "1");

    const res = await fetch(`${API}/api/tts`, { method: "POST", body: form });
    const data = await res.json();
    setTtsResult(JSON.stringify(data, null, 2));
    await loadBootData();
  }

  return (
    <main className="mx-auto min-h-screen max-w-6xl p-6">
      <header className="mb-8 rounded-2xl border-2 border-ink bg-white/70 p-6 shadow-lg">
        <h1 className="text-4xl font-bold tracking-tight">VoxCraft</h1>
        <p className="mt-2 text-sm">Offline STT/TTS platform with API support.</p>
        <p className="mt-2 text-sm">Backend health: <span className="font-semibold text-sea">{health}</span></p>
      </header>

      <section className="grid gap-6 md:grid-cols-2">
        <div className="rounded-2xl border-2 border-ink bg-white/80 p-5">
          <h2 className="text-xl font-semibold">Speech to Text</h2>
          <input className="mt-4 block w-full" type="file" accept=".mp3,.wav,.m4a,.flac" onChange={(e) => setSttFile(e.target.files?.[0] ?? null)} />
          <button className="mt-4 rounded-lg bg-accent px-4 py-2 font-semibold text-white" onClick={runSTT}>Transcribe</button>
          <pre className="mt-4 max-h-56 overflow-auto rounded bg-ink p-3 text-xs text-paper">{sttResult || "STT response will appear here."}</pre>
        </div>

        <div className="rounded-2xl border-2 border-ink bg-white/80 p-5">
          <h2 className="text-xl font-semibold">Text to Speech</h2>
          <textarea className="mt-4 w-full rounded border p-2" rows={4} value={ttsText} onChange={(e) => setTtsText(e.target.value)} />
          <select className="mt-3 w-full rounded border p-2" value={ttsVoice} onChange={(e) => setTtsVoice(e.target.value)}>
            {(models?.tts_models ?? []).map((voice) => (
              <option value={voice} key={voice}>{voice}</option>
            ))}
          </select>
          <button className="mt-4 rounded-lg bg-sea px-4 py-2 font-semibold text-white" onClick={runTTS}>Generate Audio</button>
          <pre className="mt-4 max-h-56 overflow-auto rounded bg-ink p-3 text-xs text-paper">{ttsResult || "TTS response will appear here."}</pre>
        </div>
      </section>

      <section className="mt-6 rounded-2xl border-2 border-ink bg-white/80 p-5">
        <h2 className="text-xl font-semibold">Models</h2>
        <p className="mt-2 text-sm">STT: {(models?.stt_models ?? []).join(", ")}</p>
        <p className="mt-1 text-sm">TTS: {(models?.tts_models ?? []).join(", ")}</p>
      </section>

      <section className="mt-6 rounded-2xl border-2 border-ink bg-white/80 p-5">
        <h2 className="text-xl font-semibold">Conversion History</h2>
        <div className="mt-3 space-y-2 text-sm">
          {topHistory.map((item) => (
            <div key={item.id} className="rounded border border-ink/30 bg-white p-2">
              <div>#{item.id} {item.kind.toUpperCase()} • {new Date(item.created_at).toLocaleString()}</div>
              {item.voice ? <div>Voice: {item.voice}</div> : null}
              {item.confidence !== null ? <div>Confidence: {item.confidence}</div> : null}
              {item.transcript ? <div className="line-clamp-2">Transcript: {item.transcript}</div> : null}
            </div>
          ))}
          {!topHistory.length ? <div>No history yet.</div> : null}
        </div>
      </section>
    </main>
  );
}
