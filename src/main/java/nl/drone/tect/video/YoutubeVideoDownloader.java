package nl.drone.tect.video;

import nl.drone.tect.scraper.YoutubeScraper;

/**
 * Created by Thomas on 20-3-2017.
 */
public class YoutubeVideoDownloader implements VideoDownloader {

    /**
     * The Youtube Scraper this downloader feeds off.
     */
    private YoutubeScraper scraper;


    public VideoDownloadResult downloadNext() {
        final String id = scraper.nextId();
        
        return null;
    }
}
