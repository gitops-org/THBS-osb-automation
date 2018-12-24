package com.journaldev.prime.faces.beans;

import java.io.IOException;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import javax.annotation.PostConstruct;
import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;
import javax.faces.event.ActionEvent;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.journaldev.hibernate.entity.Company;
import com.journaldev.hibernate.entity.Role;
import com.journaldev.hibernate.entity.User;
import com.journaldev.spring.service.CompanyService;
import com.journaldev.spring.service.UserWizardService;

@ManagedBean
@SessionScoped
@Component
public class CompanyController implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private Company company=new Company();
	private List<Company> companiesList = new ArrayList<>();
	private boolean editflag;
	
	
	@Autowired
	private CompanyService companyService;
	FacesMessage msg=null;
	
	
	

	public boolean isEditflag() {
		return editflag;
	}

	public void setEditflag(boolean editflag) {
		this.editflag = editflag;
	}

	
	
	@PostConstruct
	public void init() {
		try {
			setEditflag(false);
		companiesList.clear();
		companiesList = companyService.getCompaniesList();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	
	
	/**
	 * 
	 */
	public void saveCompany() {
		try {
			companyService.saveCompany(company);
			init();
			msg = new FacesMessage("Successful Created", "Company :" + company.getCompanyName());
			FacesContext.getCurrentInstance().addMessage(null, msg);

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
	
	
	
	 /**
		 * @param load the companies
		 */
		public void loadCompanies(ActionEvent e) {
			try {
				init();	
				setEditflag(false);
				ExternalContext ec = FacesContext.getCurrentInstance()
	                    .getExternalContext();
							ec.redirect(ec.getRequestContextPath()
							        + "/pages/company.xhtml");
						} catch (IOException e1) {
							// TODO Auto-generated catch block
							e1.printStackTrace();
						}
		}
		
		
		
		
		/**
		 * @param user
		 */
		public void deleteCompany(Company company) {
		    System.out.println(company);
		    try {
				companyService.deleteCompany(company);
				init();
				msg = new FacesMessage(FacesMessage.SEVERITY_INFO, "Deletion was Successful", "Deleted role is :" + company.getCompanyName());
				FacesContext.getCurrentInstance().addMessage(null, msg);
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		
		
		/**
		 * @param user
		 */
		public void editCompany(Company company) {
		    System.out.println(company);
		    try {
		    	setCompany(company);
		    	setEditflag(true);
		    	ExternalContext ec = FacesContext.getCurrentInstance()
	                    .getExternalContext();
							ec.redirect(ec.getRequestContextPath()
							        + "/pages/company.xhtml");
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		
		
		/**
		 * 
		 */
		public void addCompany() {
		    try {
		    	Company company=new Company();
		    	setCompany(company);
		    	setEditflag(false);
		    	ExternalContext ec = FacesContext.getCurrentInstance()
	                    .getExternalContext();
							ec.redirect(ec.getRequestContextPath()
							        + "/pages/company.xhtml");
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}

		public Company getCompany() {
			return company;
		}

		public void setCompany(Company company) {
			this.company = company;
		}

		public List<Company> getCompaniesList() {
			return companiesList;
		}

		public void setCompaniesList(List<Company> companiesList) {
			this.companiesList = companiesList;
		}

		public CompanyService getCompanyService() {
			return companyService;
		}

		public void setCompanyService(CompanyService companyService) {
			this.companyService = companyService;
		}

		

}