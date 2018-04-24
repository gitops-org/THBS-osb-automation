package com.javacodegeeks.example.app;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class App {
	public static void main(String[] args) {
		String[] str = {"classpath:META-INF/spring/job-config.xml","classpath:META-INF/spring/context-config.xml"};
		ApplicationContext ctx = new ClassPathXmlApplicationContext(str);		
	}
}
