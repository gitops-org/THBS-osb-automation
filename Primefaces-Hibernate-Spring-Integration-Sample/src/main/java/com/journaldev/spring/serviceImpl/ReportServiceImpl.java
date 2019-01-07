package com.journaldev.spring.serviceImpl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.journaldev.hibernate.entity.Report;
import com.journaldev.spring.dao.ReportDao;
import com.journaldev.spring.service.ReportService;

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