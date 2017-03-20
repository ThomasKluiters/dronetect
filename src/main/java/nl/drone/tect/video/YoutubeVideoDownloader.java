package nl.drone.tect.video;

import com.github.axet.vget.VGet;
import com.github.axet.vget.info.VideoFileInfo;
import com.github.axet.vget.info.VideoInfo;
import nl.drone.tect.scraper.YoutubeScraper;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Created by Thomas on 20-3-2017.
 */
public class YoutubeVideoDownloader implements VideoDownloader {

    /**
     * The Youtube Scraper this downloader feeds off.
     */
    private YoutubeScraper scraper;

    private final String sourcePattern = "https://www.youtube.com?v=%s";

    private final String destinationPattern = "/data/%s";

    public VideoDownloadResult downloadNext() {
        final String id = scraper.nextId();
        try {
            final URL source = new URL(String.format(sourcePattern, id));
            final File destination = new File(String.format(destinationPattern, id));

            VGet vGet = new VGet(source, destination);
            vGet.extract();
            vGet.download();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
        return null;
    }
}
