package nl.drone.tect.scraper;

import com.google.api.client.http.HttpRequest;
import com.google.api.client.http.HttpRequestInitializer;
import com.google.api.client.http.javanet.NetHttpTransport;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.services.youtube.YouTube;
import com.google.api.services.youtube.model.SearchListResponse;
import com.google.api.services.youtube.model.SearchResult;

import java.io.IOException;
import java.util.Collection;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

/**
 * A QueryYoutubeScraper scrapes youtube id's based on queue of queries to be executed.
 */
public class QueryYoutubeScraper implements YoutubeScraper {

    private final String secret = "AIzaSyDpp1GnliTXzWeoRuezRh_6FvaWkIP2Nis";

    private static final int DEFAULT_DEPTH = 10;

    /**
     * The queue of queries to be executed.
     */
    private BlockingQueue<String> queries;

    /**
     * The queue of ids to be streamed.
     */
    private BlockingQueue<String> ids;

    /**
     * The amount of videos the scraper will retain for each query.
     */
    private long depth;


    /**
     * Youtube Data API object to perform queries on.
     */
    private YouTube youtube;


    /**
     * Constructs a QueryYoutubeScraper with an empty queue of queries.
     */
    public QueryYoutubeScraper() {
        this(new LinkedList<String>());
    }

    /**
     * Constructs a QueryYoutubeScraper with the given collection as queries to execute.
     *
     * @param queries the queries to be executed
     */
    public QueryYoutubeScraper(Collection<String> queries) {
        this(queries, DEFAULT_DEPTH);
    }

    /**
     * Constructs a QueryYoutubeScraper with the given collection as queries to execute and depth.
     *
     * @param queries the queries to be executed
     * @param depth how many videos should be retained from each query
     */
    public QueryYoutubeScraper(Collection<String> queries, int depth) {
        this.queries = new LinkedBlockingQueue<String>(queries);
        this.ids = new LinkedBlockingQueue<>();
        this.depth = depth;

        youtube = new YouTube.Builder(new NetHttpTransport(), new JacksonFactory(), httpRequest -> {

        }).setApplicationName("School Project MMA 1").build();
    }

    /**
     * Executes the next query, will block if no queries are present.
     */
    private void executeNext() {
        final String query = queries.poll();
        if(query != null && query.length() > 0) {
            int count = 0;

            String token = null;

            do {
                try {
                    final long maxResults = Math.min(50, depth - count);

                    YouTube.Search.List search = youtube
                            .search()
                            .list("id")
                            .setQ(query)
                            .setKey(secret)
                            .setPageToken(token)
                            .setMaxResults(maxResults);

                    SearchListResponse response = search.execute();

                    List<SearchResult> items = response.getItems();
                    for (SearchResult item : items) {
                        final String id = item.getId().getVideoId();
                        ids.offer(id);
                    }

                    count += response
                            .getPageInfo()
                            .getResultsPerPage();

                    token = response.getNextPageToken();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            } while(count < depth && token != null);
        }
    }

    public String nextId() {
        if(ids.isEmpty() && !queries.isEmpty()) {
            executeNext();
        }
        return ids.poll();
    }

}
