package com.ragsInfo.serviceImpl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.ragsInfo.dao.ReportDao;
import com.ragsInfo.entity.Report;
import com.ragsInfo.service.ReportService;

@Service
public class ReportServiceImpl implements ReportService{
	

	@Autowired
	private ReportDao reportDao;

	@Override
	public List<Report> getReportsList() throws Exception {
		// TODO Auto-generated method stub
				List<Report> companiesList = reportDao.getReportsList();
				return companiesList;
	}

}