package com.journaldev.spring.dao;

import java.util.List;

import com.journaldev.hibernate.entity.Company;

public interface CompanyDao {
	
	public List<Company> getCompaniesList() throws Exception;
	
	public void saveCompany(Company company) throws Exception;

	public void deleteCompany(Company company)throws Exception;


}
