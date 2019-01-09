package com.ragsInfo.dao;

import java.util.List;

import com.ragsInfo.entity.Report;

public interface ReportDao {
	
	public List<Report> getReportsList() throws Exception;
	
}
