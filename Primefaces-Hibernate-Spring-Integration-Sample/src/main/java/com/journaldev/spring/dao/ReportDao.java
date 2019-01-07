package com.journaldev.spring.dao;

import java.util.List;

import com.journaldev.hibernate.entity.Report;

public interface ReportDao {
	
	public List<Report> getReportsList() throws Exception;
	
}
