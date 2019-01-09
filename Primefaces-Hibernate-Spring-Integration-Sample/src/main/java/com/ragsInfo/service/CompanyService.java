package com.ragsInfo.service;

import java.util.List;
import java.util.Map;

import com.ragsInfo.entity.City;
import com.ragsInfo.entity.Company;
import com.ragsInfo.entity.Country;
import com.ragsInfo.entity.State;

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