package com.journaldev.spring.daoImpl;

import java.util.List;

import org.hibernate.Criteria;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.journaldev.hibernate.entity.User;
import com.journaldev.spring.dao.UserWizardDao;

@Repository
public class UserWizardDaoImpl implements UserWizardDao {
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
	public void register(User user) throws Exception {
		// Acquire session
		Session session = sessionFactory.getCurrentSession();
		// Save employee, saving behavior get done in a transactional manner
		session.save(user);		
	}

	@Override
	@Transactional
	public List<User> getUserList() throws Exception {
		// TODO Auto-generated method stub
		Session session = sessionFactory.getCurrentSession();
		Criteria cr = session.createCriteria(User.class);
		List<User> results = cr.list();
		for (User object : results) {
			System.out.println(object);
		}
		return results;
	}

}
