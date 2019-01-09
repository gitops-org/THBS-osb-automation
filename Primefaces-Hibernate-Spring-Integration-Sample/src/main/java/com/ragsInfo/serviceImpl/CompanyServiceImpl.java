package com.ragsInfo.serviceImpl;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.ragsInfo.dao.CompanyDao;
import com.ragsInfo.entity.City;
import com.ragsInfo.entity.Company;
import com.ragsInfo.entity.Country;
import com.ragsInfo.entity.State;
import com.ragsInfo.service.CompanyService;

@Service
public class CompanyServiceImpl implements CompanyService{
	

	@Autowired
	private CompanyDao companyDao;

	@Override
	public List<Company> getCompaniesList() throws Exception {
		// TODO Auto-generated method stub
				List<Company> companiesList = companyDao.getCompaniesList();
				return companiesList;
	}

	@Override
	public void saveCompany(Company company) throws Exception {
		// TODO Auto-generated method stub
		companyDao.saveCompany(company);
	}

	@Override
	public void deleteCompany(Company company) throws Exception {
		// TODO Auto-generated method stub
		companyDao.deleteCompany(company);
	}

	@Override
	public List<State> getStates() throws Exception {
		// TODO Auto-generated method stub
	return	companyDao.getStates();
	}

	@Override
	public List<City> getCities() throws Exception {
		// TODO Auto-generated method stub
		return companyDao.getCities();
	}

	@Override
	public List<Country> getCountries() throws Exception {
		// TODO Auto-generated method stub
		return companyDao.getCountries();
	}

	@Override
	public Map<String, Integer> getStatesByCountryId(String countryId) throws Exception {
		// TODO Auto-generated method stub
		return companyDao.getStatesByCountryId(countryId);
	}
	
	
	
	@Override
	public Map<String, Integer> getCitiesByStateId(String stateId) throws Exception {
		// TODO Auto-generated method stub
		return companyDao.getCitiesByStateId(stateId);
	}
}