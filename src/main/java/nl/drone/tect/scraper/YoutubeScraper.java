package nl.drone.tect.scraper;

/**
 * A YoutubeScraper will supply a stream of String objects representing youtube videos.
 *
 * The method to acquire these ids will depend on the implementation of the scraper.
 */
public interface YoutubeScraper {

    /**
     * The scraper will return the next Youtube video id to be processed.
     *
     * The scraper may or may not be blocking.
     *
     * @return the next youtube video ID to be scraped
     */
    String nextId();

}
