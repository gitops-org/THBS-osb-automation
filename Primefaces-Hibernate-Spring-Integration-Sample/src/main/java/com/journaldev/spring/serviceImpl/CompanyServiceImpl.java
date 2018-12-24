package com.journaldev.spring.serviceImpl;

import java.util.List;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import com.journaldev.hibernate.entity.Company;
import com.journaldev.hibernate.entity.Role;
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
	
}