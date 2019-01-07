package com.journaldev.spring.service;

import java.util.List;
import java.util.Map;

import com.journaldev.hibernate.entity.City;
import com.journaldev.hibernate.entity.Company;
import com.journaldev.hibernate.entity.Country;
import com.journaldev.hibernate.entity.State;

public interface CompanyService {


	public List<Company> getCompaniesList() throws Exception;
		
	public void saveCompany(Company company) throws Exception;

	public void deleteCompany(Company company)throws Exception;

	public List<State> getStates()throws Exception;
	
	public List<City> getCities()throws Exception;
	
	public List<Country> getCountries()throws Exception;

	public Map<String, Integer> getStatesByCountryId(String country) throws Exception;

	public Map<String, Integer> getCitiesByStateId(String stateId) throws Exception;

}