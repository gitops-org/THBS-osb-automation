package com.javatpoint;

import org.apache.http.HttpHost;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.action.search.SearchType;
import org.elasticsearch.client.Client;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.index.query.QueryBuilder;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.node.Node;
import org.elasticsearch.node.NodeValidationException;

public class ElasticApiClass {

	private static Client client;
	public static void main(String[] args) throws NodeValidationException {
		// TODO Auto-generated method stub
		RestClient restClient = RestClient.builder(
			       new HttpHost("172.30.64.36", 9200, "http")).build();
		
		SearchResponse response = client.prepareSearch("application-2018.01.08", "application-2018.01.10")
		        .setTypes("application", "application")
		        .setSearchType(SearchType.DFS_QUERY_THEN_FETCH)
		        .setQuery(QueryBuilders.termQuery("multi", "test"))                 // Query
		        .setPostFilter(QueryBuilders.rangeQuery("logtime1").from("2018-01-08 11:35:17.041").to("2018-01-08 12:35:17.041"))     // Filter
		        .setFrom(0).setSize(60).setExplain(true)
		        .get();
		
		Settings settings = Settings.builder()
	            .put("path.home", "target/elasticsearch")
	            .put("transport.type", "local")
	            .put("http.enabled", false)
	            .build();
		new Node(settings).start().client();


		
		QueryBuilder qb = QueryBuilders.termQuery("name", "some string");
		response = client.prepareSearch("index") //
		    .setQuery(qb) // Query
		    .execute().actionGet();
	}
	 
}
