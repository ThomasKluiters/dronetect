package nl.drone.tect;

import com.google.common.collect.Lists;
import nl.drone.tect.converter.VideoConverter;
import nl.drone.tect.converter.YoutubeVideoConverter;
import nl.drone.tect.scraper.ListYoutubeScraper;
import nl.drone.tect.scraper.QueryYoutubeScraper;
import nl.drone.tect.scraper.YoutubeScraper;
import nl.drone.tect.video.VideoDownloadResult;
import nl.drone.tect.video.VideoDownloader;
import nl.drone.tect.video.YoutubeVideoDownloader;

import java.util.Arrays;
import java.util.List;

/**
 * Created by Thomas on 20-3-2017.
 */
public class Main {

    public static void main(String[] args) {
        List<String> ids = Arrays.asList("mVPFsXI5nJc", "VwqKn1ziC0s");
        YoutubeScraper scraper = new ListYoutubeScraper(ids);
        VideoDownloader downloader = new YoutubeVideoDownloader(scraper);
        YoutubeVideoConverter converter = new YoutubeVideoConverter(500);
        converter.init();

        for (int i = 0; i < 3; i++) {
            VideoDownloadResult result = downloader.downloadNext();
            converter.convert(result.getId());
        }

    }

}
