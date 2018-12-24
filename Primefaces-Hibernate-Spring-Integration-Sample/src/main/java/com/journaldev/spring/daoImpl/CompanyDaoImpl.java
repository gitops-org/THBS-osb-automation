package com.journaldev.spring.daoImpl;

import java.util.List;

import org.hibernate.Criteria;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.journaldev.hibernate.entity.Company;
import com.journaldev.hibernate.entity.Role;
import com.journaldev.hibernate.entity.User;
import com.journaldev.spring.dao.CompanyDao;
import com.journaldev.spring.dao.UserWizardDao;

@Repository
public class CompanyDaoImpl implements CompanyDao {
	@Autowired
	private SessionFactory sessionFactory;

	public SessionFactory getSessionFactory() {
		return sessionFactory;
	}

	public void setSessionFactory(SessionFactory sessionFactory) {
		this.sessionFactory = sessionFactory;
	}

	@Override
	@Transactional
	public List<Company> getCompaniesList() throws Exception {
		Session session = sessionFactory.getCurrentSession();
		Criteria cr = session.createCriteria(Company.class);
		List<Company> results = cr.list();
		return results;
	}

	@Override
	@Transactional
	public void saveCompany(Company company) throws Exception {
		Session session = sessionFactory.getCurrentSession();
		// Save employee, saving behavior get done in a transactional manner
		session.saveOrUpdate(company);	
	}

	@Override
	@Transactional
	public void deleteCompany(Company company) throws Exception {
		// TODO Auto-generated method stub
		// Acquire session
				Session session = sessionFactory.getCurrentSession();
				// Save employee, saving behavior get done in a transactional manner
				session.delete(company);
	}



	
}
