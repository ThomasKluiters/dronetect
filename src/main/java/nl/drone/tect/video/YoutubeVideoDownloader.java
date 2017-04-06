package nl.drone.tect.video;

import com.sapher.youtubedl.YoutubeDL;
import com.sapher.youtubedl.YoutubeDLException;
import com.sapher.youtubedl.YoutubeDLRequest;
import com.sapher.youtubedl.YoutubeDLResponse;
import nl.drone.tect.scraper.YoutubeScraper;

/**
 * Created by Thomas on 20-3-2017.
 */
public class YoutubeVideoDownloader implements VideoDownloader {

    /**
     * The Youtube Scraper this downloader feeds off.
     */
    private YoutubeScraper scraper;

    private final String sourcePattern = "https://www.youtube.com/watch?v=%s";

    private final String destinationPattern = "data/%s";

    public YoutubeVideoDownloader(YoutubeScraper scraper) {
        this.scraper = scraper;
    }

    public void initialize() {
        final File dataDirectory = new File("data");
        if(!dataDirectory.isDirectory() || !dataDirectory.exists()) {
            if(!dataDirectory.mkdir()) {
                throw new RuntimeException("Could not create the data directory.");
            }
        }
    }

    public VideoDownloadResult downloadNext() {
        try {
            final String id = scraper.nextId();
            String video = String.format(sourcePattern, id);
            String directory = String.format(destinationPattern, id);
            //C:\Python27>youtube-dl.exe -f bestaudio,bestvideo https://www.youtube.com/watch?v=y-rEI4bezWc&t=2
            YoutubeDLRequest videoRequest = new YoutubeDLRequest(video, directory);
            videoRequest.setOption("format", "bestvideo");
            videoRequest.setOption("output", "video.%(ext)s");

            YoutubeDLRequest audioRequest = new YoutubeDLRequest(video, directory);
            audioRequest.setOption("format", "bestaudio");
            audioRequest.setOption("output", "audio.%(ext)s");

            YoutubeDL.execute(audioRequest);
            YoutubeDL.execute(videoRequest);
            return new VideoDownloadResult(id);
        } catch (YoutubeDLException e) {
            e.printStackTrace();
        }
        return null;
    }
}
