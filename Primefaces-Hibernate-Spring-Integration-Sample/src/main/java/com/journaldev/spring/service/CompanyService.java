package com.journaldev.spring.service;

import java.util.List;

import com.journaldev.hibernate.entity.Company;

public interface CompanyService {


	public List<Company> getCompaniesList() throws Exception;
		
	public void saveCompany(Company company) throws Exception;

	public void deleteCompany(Company company)throws Exception;

}