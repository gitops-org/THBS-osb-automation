package com.ragsInfo.controller;

import java.io.IOException;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import javax.annotation.PostConstruct;
import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.RequestScoped;
import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;
import javax.faces.event.ActionEvent;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.ragsInfo.entity.City;
import com.ragsInfo.entity.Company;
import com.ragsInfo.entity.Country;
import com.ragsInfo.entity.State;
import com.ragsInfo.service.CompanyService;

@ManagedBean
@RequestScoped
@Component
public class CompanyController implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private Company company=new Company();
	private List<Company> companiesList = new ArrayList<>();
	private boolean editflag;
	private Map<String,Integer> countries;
    private Map<String,Integer> cities;
    private Map<String,Integer> states;
	
    
    
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
		populateDataList();
		companiesList = companyService.getCompaniesList();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	
	
	private void populateDataList() {
		// TODO Auto-generated method stub
		try {
		List<State> statesList = companyService.getStates();
		states=statesList.stream().collect(Collectors.toMap(State::getState, State::getStateId));
		List<Country> countriesList = companyService.getCountries();
		countries=countriesList.stream().collect(Collectors.toMap(Country::getCountry,Country:: getCountryId));
		List<City> citiesList = companyService.getCities();
		cities=citiesList.stream().collect(Collectors.toMap(City::getCity, City::getCityId));
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
			System.out.println(company);
			Country country=new Country();
			country.setCountryId(Integer.parseInt(company.getCountryName()));
			getCompany().setCountry(country);
			City city=new City();
			city.setCityId(Integer.parseInt(company.getCityName()));
			getCompany().setCity(city);
			State state =new State();
			state.setStateId(Integer.parseInt(company.getStateName()));
			getCompany().setState(state);
			companyService.saveCompany(getCompany());
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
		    	company.setCountryName(String.valueOf(company.getCountry().getCountryId()));
		    	company.setStateName(String.valueOf(company.getState().getStateId()));
		    	company.setCityName(String.valueOf(company.getCity().getCityId()));
		    	setEditflag(true);
		    	populateDataList();
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

		
		 /**
		 * to get the statelist
		 */
		public void onCountryChange() {
		try {
			if (getCompany().getCountryName() != null && !getCompany().getCountryName().equals("")) {
				System.out.println("*******************************************"+getCompany().getCountryName());
				states = companyService.getStatesByCountryId(getCompany().getCountryName());
			} else {
				states = new HashMap<String, Integer>();
			}

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		 
		}
		 /**
		 * to get the cities list
		 */
		public void onStateChange() {
			try {
				if (getCompany().getStateName() != null && !getCompany().getStateName().equals("")) {
					cities = companyService.getCitiesByStateId(getCompany().getStateName());
				} else {
					cities = new HashMap<String, Integer>();
				}

			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			 
			}


		 /**
		 * setter and getter methods
		 */
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

		public Map<String, Integer> getCountries() {
			return countries;
		}

		public void setCountries(Map<String, Integer> countries) {
			this.countries = countries;
		}

		public Map<String, Integer> getCities() {
			return cities;
		}

		public void setCities(Map<String, Integer> cities) {
			this.cities = cities;
		}

		public Map<String, Integer> getStates() {
			return states;
		}

		public void setStates(Map<String, Integer> states) {
			this.states = states;
		}

		

}