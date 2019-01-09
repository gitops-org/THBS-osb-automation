package com.ragsInfo.daoImpl;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.hibernate.Criteria;
import org.hibernate.FetchMode;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.criterion.Restrictions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.ragsInfo.dao.CompanyDao;
import com.ragsInfo.entity.City;
import com.ragsInfo.entity.Company;
import com.ragsInfo.entity.Country;
import com.ragsInfo.entity.State;

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
		Criteria cr = session.createCriteria(Company.class,"company")
				.setFetchMode("country",  FetchMode.JOIN).setFetchMode("state", FetchMode.JOIN).setFetchMode("city", FetchMode.JOIN);
		List<Company> companies = cr.list();
		return companies;
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

	@Override
	@Transactional
	public List<State> getStates() throws Exception {
		Session session = sessionFactory.getCurrentSession();
		Criteria cr = session.createCriteria(State.class);
		List<State> results = cr.list();
		return results;
	}

	@Override
	@Transactional
	public List<City> getCities() throws Exception {
		Session session = sessionFactory.getCurrentSession();
		Criteria cr = session.createCriteria(City.class);
		List<City> results = cr.list();
		return results;
	}

	@Override
	@Transactional
	public List<Country> getCountries() throws Exception {
		// TODO Auto-generated method stub
		Session session = sessionFactory.getCurrentSession();
		Criteria cr = session.createCriteria(Country.class);
		List<Country> results = cr.list();
		return results;
	}

	@Override
	@Transactional
	public Map<String, Integer> getStatesByCountryId(String countryName) throws Exception {
		// TODO Auto-generated method stub
		Session session = sessionFactory.getCurrentSession();
		Criteria cr = session.createCriteria(State.class);
		cr.add(Restrictions.eq("country.countryId",Integer.parseInt(countryName)));
		List<State> results = cr.list();
    return results.stream().collect(Collectors.toMap(State::getState,State::getStateId));
	}
	
	
	@Override
	@Transactional
	public Map<String, Integer> getCitiesByStateId(String stateId) throws Exception {
		// TODO Auto-generated method stub
		Session session = sessionFactory.getCurrentSession();
		Criteria cr = session.createCriteria(City.class);
		cr.add(Restrictions.eq("state.stateId", Integer.parseInt(stateId)));
		List<City> results = cr.list();
    return results.stream().collect(Collectors.toMap(City::getCity,City::getCityId));
	}



	
}
