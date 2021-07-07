package com.mozilla.contextualservices.latency_test;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.HashMap;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CounterController {

    private final ConcurrentMap<String, Integer> counters = new ConcurrentHashMap<>();

    Logger logger = LoggerFactory.getLogger(CounterController.class);

    @GetMapping("/{name}")
    public Map<String, Integer> greeting(@PathVariable(value = "name") String name)
    {
        // try {
        //     Thread.sleep(1000);
        // } catch (InterruptedException e) {
        // }

        Integer count = counters.compute(name, (key, oldCount) -> {
            if (oldCount == null) {
                return 1;
            } else {
                return oldCount + 1;
            }
        });
        logger.info(String.format("Incremented %s to %d", name, count));

        Map<String, Integer> result = new HashMap<>();
        result.put(name, count);
        return result;
    }
}
