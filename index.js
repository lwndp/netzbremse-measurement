import SpeedTest from '@cloudflare/speedtest';

console.log('Starting speed test...\n');

const url = "https://custom-t0.speed.cloudflare.com"
const config = {
    downloadApiUrl: `${url}/__down`,
    uploadApiUrl: `${url}/__up`,
    turnServerCredsApiUrl: `${url}/__turn`,
    turnServerUri: "turn.cloudflare.com:3478",
    includeCredentials: false,
    measurements: [
        { type: "download", bytes: 100_000, count: 2 },
        { type: "upload", bytes: 100_000, count: 2 },
        { type: "download", bytes: 10_000_000, count: 2 },
        { type: "upload", bytes: 5_000_000, count: 2 },
        { type: "download", bytes: 25_000_000, count: 2 },
        { type: "upload", bytes: 10_000_000, count: 2 },
        { type: "latency", numPackets: 40 },
    ],
    loadedLatencyThrottle: 300,
}

const speedTest = new SpeedTest(config);

const results = await new Promise(resolve => {
    speedTest.onFinish = (results) => resolve(results);
});

const summary = results.getSummary();

console.log('Results:');
console.log(`Download: ${Math.round(summary.download / 1e6)} Mbps`);
console.log(`  Latency: ${Math.round(summary.downLoadedLatency)} ms`)
console.log(`  Jitter: ${Math.round(summary.downLoadedJitter)} ms`)
console.log(`Upload: ${Math.round(summary.upload / 1e6)} Mbps`);
console.log(`  Latency: ${Math.round(summary.upLoadedLatency)} ms`)
console.log(`  Jitter: ${Math.round(summary.upLoadedJitter)} ms`)
console.log('Idle:');
console.log(`  Latency: ${Math.round(summary.latency)} ms`);
console.log(`  Jitter: ${Math.round(summary.jitter)} ms`);
