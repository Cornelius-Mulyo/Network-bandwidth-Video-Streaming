from flask import Flask, send_file, request, jsonify
from datetime import datetime
import csv
import os

app = Flask(__name__)

videos = {
    "480p": "videos/lesson1/480p/lesson1_480p.mp4",
    "720p": "videos/lesson1/720p/lesson1_720p.mp4",
    "1080p": "videos/lesson1/1080p/lesson1_1080p.mp4"
}

# Research data location
DATA_DIR = "research/data/raw"
CSV_FILE = os.path.join(DATA_DIR, "video_trials.csv")

os.makedirs(DATA_DIR, exist_ok=True)

CSV_FIELDS = [
    "trial",
    "timestamp",
    "quality",
    "bandwidth_mbps",
    "observation_seconds",
    "startup_time_seconds",
    "buffering_occurred",
    "buffer_events",
    "total_buffering_seconds",
    "first_buffer_time_seconds"
]


def get_next_trial_number():
    if not os.path.exists(CSV_FILE):
        return 1

    with open(CSV_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    return len(rows) + 1


def save_trial(data):
    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)


@app.route("/")
def home():
    return """
    <h1>Raspberry Pi Edge Media Server</h1>

    <h3>Lesson 1</h3>

    <ul>
        <li><a href="/video/480p">480p</a></li>
        <li><a href="/video/720p">720p</a></li>
        <li><a href="/video/1080p">1080p</a></li>
    </ul>

    <h3>Research Measurement</h3>

    <ul>
        <li><a href="/test/480p">Test 480p</a></li>
        <li><a href="/test/720p">Test 720p</a></li>
        <li><a href="/test/1080p">Test 1080p</a></li>
    </ul>
    """


@app.route("/video/<quality>")
def video(quality):
    if quality not in videos:
        return "Video quality not found", 404

    return send_file(videos[quality])


@app.route("/record", methods=["POST"])
def record():
    data = request.get_json()

    trial_number = get_next_trial_number()

    record_data = {
        "trial": trial_number,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "quality": data["quality"],
        "bandwidth_mbps": data["bandwidth"],
        "observation_seconds": data["observation_seconds"],
        "startup_time_seconds": data["startup_time"],
        "buffering_occurred": data["buffering_occurred"],
        "buffer_events": data["buffer_events"],
        "total_buffering_seconds": data["total_buffering_seconds"],
        "first_buffer_time_seconds": data["first_buffer_time_seconds"]
    }

    save_trial(record_data)

    return jsonify({
        "success": True,
        "trial": trial_number
    })


@app.route("/test/<quality>")
def test(quality):
    if quality not in videos:
        return "Video quality not found", 404

    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>Research Test - {quality}</title>
    </head>

    <body>

        <h1>Lesson 1 - {quality}</h1>

        <p>
            <strong>Research Trial</strong>
        </p>

        <label for="bandwidth">
            Bandwidth condition:
        </label>

        <select id="bandwidth">
            <option value="26">26 Mbps</option>
            <option value="10">10 Mbps</option>
            <option value="5">5 Mbps</option>
            <option value="2">2 Mbps</option>
            <option value="1">1 Mbps</option>
        </select>

        <p>
            Startup time:
            <strong id="startup">Waiting...</strong>
        </p>

        <p>
            Buffering events:
            <strong id="buffers">0</strong>
        </p>

        <p>
            Buffering occurred:
            <strong id="buffering">No</strong>
        </p>

        <p>
            Total buffering time:
            <strong id="bufferTime">0.000 seconds</strong>
        </p>

        <p>
            First buffering event:
            <strong id="firstBuffer">None</strong>
        </p>

        <p>
            Observation:
            <strong id="observation">Waiting...</strong>
        </p>

        <p>
            Status:
            <strong id="status">
                Waiting for video request...
            </strong>
        </p>

        <video
            id="video"
            controls
            autoplay
            muted
            playsinline
            width="800"
        >
            <source src="/video/{quality}" type="video/mp4">
        </video>

        <script>

            const video = document.getElementById("video");
            const startup = document.getElementById("startup");
            const buffers = document.getElementById("buffers");
            const buffering = document.getElementById("buffering");
            const bufferTime = document.getElementById("bufferTime");
            const firstBuffer = document.getElementById("firstBuffer");
            const observation = document.getElementById("observation");
            const status = document.getElementById("status");
            const bandwidth = document.getElementById("bandwidth");

            const quality = "{quality}";

            const OBSERVATION_SECONDS = 60;

            let requestTime = null;
            let startupTime = null;

            let hasStarted = false;

            let bufferEvents = 0;

            let isBuffering = false;

            let bufferStartTime = null;

            let totalBufferingSeconds = 0;

            let firstBufferTimeSeconds = null;

            let observationStarted = false;

            let observationStartTime = null;

            let observationTimer = null;


            /*
             * Browser begins requesting the video.
             */
            video.addEventListener("loadstart", function() {{

                requestTime = performance.now();

                status.textContent =
                    "Video requested. Waiting for playback...";

            }});


            /*
             * Video begins playing.
             */
            video.addEventListener("playing", function() {{

                /*
                 * Measure startup time.
                 */
                if (requestTime !== null && startupTime === null) {{

                    const playTime = performance.now();

                    startupTime =
                        (playTime - requestTime) / 1000;

                    startup.textContent =
                        startupTime.toFixed(3) + " seconds";

                    hasStarted = true;

                    status.textContent =
                        "Video is playing.";

                }}


                /*
                 * A playing event after waiting means
                 * buffering has ended.
                 */
                if (isBuffering && bufferStartTime !== null) {{

                    const bufferEndTime = performance.now();

                    const bufferingDuration =
                        (bufferEndTime - bufferStartTime) / 1000;

                    totalBufferingSeconds +=
                        bufferingDuration;

                    bufferTime.textContent =
                        totalBufferingSeconds.toFixed(3)
                        + " seconds";

                    isBuffering = false;

                    bufferStartTime = null;

                    status.textContent =
                        "Video resumed after buffering.";

                }}


                /*
                 * Start the observation period.
                 */
                if (!observationStarted) {{

                    observationStarted = true;

                    observationStartTime =
                        performance.now();

                    let seconds = 0;

                    observation.textContent =
                        "0 / "
                        + OBSERVATION_SECONDS
                        + " seconds";

                    observationTimer =
                        setInterval(function() {{

                            seconds++;

                            observation.textContent =
                                seconds
                                + " / "
                                + OBSERVATION_SECONDS
                                + " seconds";

                            if (seconds >= OBSERVATION_SECONDS) {{

                                clearInterval(observationTimer);

                                finishTrial();

                            }}

                        }}, 1000);
                }}

            }});


            /*
             * Browser is waiting for more video data.
             */
            video.addEventListener("waiting", function() {{

                /*
                 * Only count buffering after
                 * playback has started.
                 */
                if (hasStarted && !isBuffering) {{

                    bufferEvents++;

                    buffers.textContent =
                        bufferEvents;

                    buffering.textContent =
                        "Yes";

                    isBuffering = true;

                    bufferStartTime =
                        performance.now();

                    /*
                     * Time from beginning of the
                     * observation until first buffer.
                     */
                    if (firstBufferTimeSeconds === null) {{

                        firstBufferTimeSeconds =
                            (performance.now()
                            - observationStartTime) / 1000;

                        firstBuffer.textContent =
                            firstBufferTimeSeconds.toFixed(3)
                            + " seconds";

                    }}

                    status.textContent =
                        "Buffering...";

                }}

            }});


            /*
             * Video can play.
             */
            video.addEventListener("canplay", function() {{

                if (!hasStarted) {{

                    status.textContent =
                        "Video can play. Waiting for playback...";

                }}

            }});


            /*
             * Finish the trial.
             */
            function finishTrial() {{

                /*
                 * If the trial ends while buffering,
                 * close the final buffering interval.
                 */
                if (isBuffering && bufferStartTime !== null) {{

                    const finalBufferTime =
                        performance.now();

                    totalBufferingSeconds +=
                        (finalBufferTime - bufferStartTime) / 1000;

                    bufferTime.textContent =
                        totalBufferingSeconds.toFixed(3)
                        + " seconds";

                    isBuffering = false;

                }}

                video.pause();

                status.textContent =
                    "Trial complete. Saving results...";

                const data = {{

                    quality: quality,

                    bandwidth:
                        Number(bandwidth.value),

                    observation_seconds:
                        OBSERVATION_SECONDS,

                    startup_time:
                        startupTime,

                    buffering_occurred:
                        bufferEvents > 0 ? "Yes" : "No",

                    buffer_events:
                        bufferEvents,

                    total_buffering_seconds:
                        totalBufferingSeconds,

                    first_buffer_time_seconds:
                        firstBufferTimeSeconds

                }};


                fetch("/record", {{

                    method: "POST",

                    headers: {{
                        "Content-Type":
                            "application/json"
                    }},

                    body:
                        JSON.stringify(data)

                }})

                .then(response =>
                    response.json()
                )

                .then(result => {{

                    status.textContent =
                        "Trial "
                        + result.trial
                        + " saved successfully.";

                }})

                .catch(error => {{

                    console.error(error);

                    status.textContent =
                        "ERROR: Could not save trial.";

                }});

            }}

        </script>

    </body>

    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
