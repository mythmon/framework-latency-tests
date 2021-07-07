package com.mozilla.contextualservices.latency_test;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class LatencyTestApplication {

	public static void main(String[] args) {
		SpringApplication.run(LatencyTestApplication.class, args);
	}
}
