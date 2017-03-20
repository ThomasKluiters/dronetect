package nl.drone.tect.scene;

import com.sun.istack.internal.NotNull;
import net.bramp.ffmpeg.FFmpeg;
import net.bramp.ffmpeg.FFprobe;
import net.bramp.ffmpeg.ProcessFunction;
import net.bramp.ffmpeg.RunProcessFunction;
import net.bramp.ffmpeg.info.Format;
import net.bramp.ffmpeg.probe.FFmpegFormat;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by Thomas on 20-3-2017.
 */
public class SceneDetector {

    private static final String DEFAULT_FFMPEG_PATH = "tools/ffmpeg.exe";
    private static final String DEFAULT_FFPROBE_PATH = "tools/ffprobe.exe";

    /**
     * The ffmpeg object.
     */
    private FFmpeg ffmpeg = null;

    /**
     * The ffprobe object.
     */
    private FFprobe ffprobe = null;

    /**
     * The path to the ffmpeh executable.
     */
    private final String ffmpegPath;

    /**
     * The path to the ffprobe executable.
     */
    private final String ffprobePath;

    private final String videoFormat = "\"movie=%s,select=gt(scene\\,0.3)\"";

    private final String sceneRegex = "best_effort_timestamp=([0-9]+)";

    private final Pattern scenePattern = Pattern.compile(sceneRegex);

    /**
     * Constructs a Scene Detector object with default FFprobe and FFmpeg paths.
     */
    public SceneDetector() {
        this(DEFAULT_FFMPEG_PATH, DEFAULT_FFPROBE_PATH);
    }

    /**
     * Constructs a Scene Detector object with the given ffmpegPath and ffprobePath.
     *
     * @param ffmpegPath
     * @param ffprobePath
     */
    public SceneDetector(@NotNull String ffmpegPath, @NotNull String ffprobePath) {
        this.ffmpegPath = ffmpegPath;
        this.ffprobePath = ffprobePath;
    }

    /**
     *  Initializes this scene detector with the given ffmpeg and ffprobe paths.
     */
    public void initialize() {
        try {
            ProcessFunction function = new SceneProcessFunction();

            ffmpeg = new FFmpeg(ffmpegPath);
            ffprobe = new FFprobe(ffprobePath, function);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    /**
     * Processes the given video and makes an attempt to detect scene changes.
     *
     * @param video the video path to analyse
     */
    public void process(@NotNull final String video) {
        try {
            List<String> args = Arrays.asList(
                    ffprobePath,
                    "-show_frames",
                    "-of",
                    "compact=p=0",
                    "-f",
                    "lavfi",
                    String.format(videoFormat, video)
            );

            Process process = new RunProcessFunction().run(args);
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8));

            String in = null;
            while((in = reader.readLine()) != null) {
                final Matcher matcher = scenePattern.matcher(in);
                if(matcher.find()) {
                    final String timestamp = matcher.group(1);
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    class SceneProcessFunction extends RunProcessFunction {

        @Override
        public Process run(List<String> args) throws IOException {
            return super.run(args);
        }
    }

}
