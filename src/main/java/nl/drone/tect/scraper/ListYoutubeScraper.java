package nl.drone.tect.scraper;

import java.util.Collection;
import java.util.Iterator;

/**
 * Created by Thomas on 20-3-2017.
 */
public class ListYoutubeScraper implements YoutubeScraper {

    /**
     * The Iterator this Scraper will iterate over.
     */
    private Iterator<String> ids;

    /**
     * Constructs a scraper with the given Collection of youtube video ids.
     *
     * @param ids the collection of video ids
     */
    public ListYoutubeScraper(final Collection<String> ids) {
        this.ids = ids.iterator();
    }

    @Override
    public String nextId() {
        if(ids.hasNext()) {
           return ids.next();
        }
        return null;
    }
}
