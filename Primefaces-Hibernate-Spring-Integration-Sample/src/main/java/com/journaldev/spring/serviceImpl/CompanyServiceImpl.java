package com.journaldev.spring.serviceImpl;

import java.util.List;
import java.util.Map;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import com.journaldev.hibernate.entity.City;
import com.journaldev.hibernate.entity.Company;
import com.journaldev.hibernate.entity.Country;
import com.journaldev.hibernate.entity.Role;
import com.journaldev.hibernate.entity.State;
import com.journaldev.hibernate.entity.User;
import com.journaldev.spring.dao.CompanyDao;
import com.journaldev.spring.dao.UserWizardDao;
import com.journaldev.spring.service.CompanyService;
import com.journaldev.spring.service.UserWizardService;

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