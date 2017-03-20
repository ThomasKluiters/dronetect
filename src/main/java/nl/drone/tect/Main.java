package nl.drone.tect;

import com.google.common.collect.Lists;
import nl.drone.tect.scraper.ListYoutubeScraper;
import nl.drone.tect.scraper.QueryYoutubeScraper;
import nl.drone.tect.video.YoutubeVideoDownloader;

import java.util.Arrays;

/**
 * Created by Thomas on 20-3-2017.
 */
public class Main {

    public static void main(String[] args) {
        YoutubeVideoDownloader downloader = new YoutubeVideoDownloader(new QueryYoutubeScraper(Arrays.asList("drone audio test")));
        downloader.initialize();
        downloader.downloadNext();
    }

}
