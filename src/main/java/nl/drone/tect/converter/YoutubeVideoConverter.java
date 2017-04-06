package nl.drone.tect.converter;

import net.bramp.ffmpeg.FFmpeg;
import net.bramp.ffmpeg.FFmpegExecutor;
import net.bramp.ffmpeg.FFprobe;
import net.bramp.ffmpeg.builder.FFmpegBuilder;
import net.bramp.ffmpeg.probe.FFmpegFormat;

import java.io.File;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

/**
 * Created by Thomas on 30-3-2017.
 */
public class YoutubeVideoConverter implements VideoConverter {

    private FFmpeg ffmpeg;
    private FFprobe ffprobe;

    FFmpegExecutor executor;

    private final long duration;

    public YoutubeVideoConverter() {
        this(2000);
    }

    public YoutubeVideoConverter(long duration) {
        this.duration = duration;
    }

    public void init() {
        try {
            ffmpeg = new FFmpeg("ffmpeg.exe");
            ffprobe = new FFprobe("ffprobe.exe");
            executor = new FFmpegExecutor(ffmpeg, ffprobe);
            if (!new File("data/scenes").exists()) {
                new File("data/scenes").mkdir();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void convert(String id) {
        try {
            String audioPath = null;
            String videoPath = null;

            File file = new File("data/" + id);
            for (File data : file.listFiles()) {
                if(data.getName().contains("audio")) {
                    audioPath = data.getPath();
                }
                if(data.getName().contains("video")) {
                    videoPath = data.getPath();
                }
            }

            System.out.println(audioPath);

            FFmpegFormat videoFormat = ffprobe.probe(videoPath).getFormat();
            FFmpegFormat audioFormat = ffprobe.probe(audioPath).getFormat();

            final String path = "data/scenes/" + id;
            if(new File(path).mkdir()) {

                System.out.println(audioFormat.duration);
                System.out.println(videoFormat.duration);

                double maxDuration = videoFormat.duration;
                double from = 0;

                final double duration = this.duration / 1000.0;
                while (from < videoFormat.duration) {

                    FFmpegBuilder videoBuilder = ffmpeg.builder().addInput(videoPath);
                    FFmpegBuilder audioBuilder = ffmpeg.builder().addInput(audioPath);

                    for (int i = 0; i < 200; i++) {
                        final double to = Math.min(from + duration, maxDuration);

                        final long toMillis = (long) (to * 1000);
                        final long fromMillis = (long) (from * 1000);

                        if (toMillis - fromMillis < 0) {
                            continue;
                        }

                        audioBuilder.addOutput(String.format("%s/%s-%d-%d.wav", path, id, fromMillis, toMillis))
                                .setFormat("wav")
                                .setStartOffset(fromMillis, TimeUnit.MILLISECONDS)
                                .setDuration(toMillis - fromMillis, TimeUnit.MILLISECONDS)
                                .done();

                        videoBuilder.addOutput(String.format("%s/%s-%d-%d.avi", path, id, fromMillis, toMillis))
                                .setFormat("avi")
                                .setStartOffset(fromMillis, TimeUnit.MILLISECONDS)
                                .setDuration(toMillis - fromMillis, TimeUnit.MILLISECONDS)
                                .done();

                        from += duration;
                    }

                    executor.createJob(videoBuilder).run();
                    executor.createJob(audioBuilder).run();

                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
