package com.journaldev.spring.service;

import java.util.List;

import com.journaldev.hibernate.entity.Report;

public interface ReportService {

	public List<Report> getReportsList() throws Exception;
		
}