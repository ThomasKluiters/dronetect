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

/**
 * Created by Thomas on 20-3-2017.
 */
public class Main {

    public static void main(String[] args) {
        YoutubeScraper scraper = new ListYoutubeScraper(Arrays.asList("y-rEI4bezWc"));
        VideoDownloader downloader = new YoutubeVideoDownloader(scraper);
        VideoDownloadResult result = downloader.downloadNext();
        YoutubeVideoConverter converter = new YoutubeVideoConverter();
        converter.init();
        converter.convert(result.getId());
    }

}
