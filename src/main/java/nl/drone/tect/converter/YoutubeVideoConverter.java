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

    public void init() {
        try {
            ffmpeg = new FFmpeg("ffmpeg.exe");
            ffprobe = new FFprobe("ffprobe.exe");
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


            FFmpegFormat format = ffprobe.probe(videoPath).getFormat();
            FFmpegBuilder videoBuilder = ffmpeg.builder().addInput(videoPath);
            FFmpegBuilder audioBuilder = ffmpeg.builder().addInput(audioPath);

            final int duration = (int) Math.floor(format.duration);
            for (int from = 0; from < duration; from += 2) {
                final int to = Math.min(from + 2, duration);

                audioBuilder.addOutput(String.format("data/scenes/%s-%d-%d.wav", id, from, to))
                        .setStartOffset(from, TimeUnit.SECONDS)
                        .setDuration(to - from, TimeUnit.SECONDS)
                        .done();

                videoBuilder.addOutput(String.format("data/scenes/%s-%d-%d.avi", id , from, to))
                        .setFormat("avi")
                        .setStartOffset(from, TimeUnit.SECONDS)
                        .setDuration(to - from, TimeUnit.SECONDS)
                        .done();
            }

            FFmpegExecutor executor = new FFmpegExecutor(ffmpeg, ffprobe);
            executor.createJob(videoBuilder).run();
            executor.createJob(audioBuilder).run();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
