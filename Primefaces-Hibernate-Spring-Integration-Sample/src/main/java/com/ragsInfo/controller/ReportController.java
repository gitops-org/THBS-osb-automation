package com.ragsInfo.controller;

import java.io.IOException;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import javax.annotation.PostConstruct;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.RequestScoped;
import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;
import javax.faces.event.ActionEvent;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.ragsInfo.Utility.MailSenderUtils;
import com.ragsInfo.entity.Report;
import com.ragsInfo.entity.ReportData;
import com.ragsInfo.service.ReportService;

@ManagedBean
@RequestScoped
@Component
public class ReportController implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private ReportData reportData = new ReportData();
	private List<Report> reportList = new ArrayList<>();
	private Map<String,Integer> reportNames;
	
	@Autowired
	private ReportService reportService;
	
	@Autowired
	MailSenderUtils mailSenderUtils;

	public MailSenderUtils getMailSenderUtils() {
		return mailSenderUtils;
	}

	public void setMailSenderUtils(MailSenderUtils mailSenderUtils) {
		this.mailSenderUtils = mailSenderUtils;
	}

	public ReportService getReportService() {
		return reportService;
	}

	public void setReportService(ReportService reportService) {
		this.reportService = reportService;
	}

	public Map<String, Integer> getReportNames() {
		return reportNames;
	}

	public void setReportNames(Map<String, Integer> reportNames) {
		this.reportNames = reportNames;
	}

	public ReportData getReportData() {
		return reportData;
	}

	public void setReportData(ReportData reportData) {
		this.reportData = reportData;
	}

	public List<Report> getReportList() {
		return reportList;
	}

	public void setReportList(List<Report> reportList) {
		this.reportList = reportList;
	}

	@PostConstruct
	public void init() {
		try {
		reportList.clear();
		 reportList = reportService.getReportsList();
		 reportNames=reportList.stream().collect(Collectors.toMap(Report::getOppId, Report::getReportId));
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	/**
	 * @param load
	 *            the roles
	 */
	public void loadReports(ActionEvent e) {
		try {
			init();
			//mailSenderUtils.sendMail();
			ExternalContext ec = FacesContext.getCurrentInstance().getExternalContext();
			ec.redirect(ec.getRequestContextPath() + "/pages/report.xhtml");
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
	}

}