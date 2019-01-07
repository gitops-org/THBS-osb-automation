package com.journaldev.prime.faces.beans;

import java.io.IOException;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import javax.annotation.PostConstruct;
import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.RequestScoped;
import javax.faces.bean.SessionScoped;
import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;
import javax.faces.event.ActionEvent;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.journaldev.hibernate.entity.Report;
import com.journaldev.hibernate.entity.ReportData;
import com.journaldev.hibernate.entity.Role;
import com.journaldev.spring.service.CompanyService;
import com.journaldev.spring.service.ReportService;
import com.journaldev.spring.service.UserWizardService;

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

	@Autowired
	private ReportService reportService;

	public ReportService getReportService() {
		return reportService;
	}

	public void setReportService(ReportService reportService) {
		this.reportService = reportService;
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
			ExternalContext ec = FacesContext.getCurrentInstance().getExternalContext();
			ec.redirect(ec.getRequestContextPath() + "/pages/report.xhtml");
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
	}

}