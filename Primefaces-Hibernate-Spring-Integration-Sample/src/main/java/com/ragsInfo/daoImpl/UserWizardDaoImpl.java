package com.ragsInfo.daoImpl;

import java.util.List;

import org.hibernate.Criteria;
import org.hibernate.FetchMode;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.ragsInfo.dao.UserWizardDao;
import com.ragsInfo.entity.Role;
import com.ragsInfo.entity.Tagging;
import com.ragsInfo.entity.User;

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
		session.saveOrUpdate(user);		
	}

	@Override
	@Transactional
	public List<User> getUserList() throws Exception {
		// TODO Auto-generated method stub
		Session session = sessionFactory.getCurrentSession();
		Criteria cr = session.createCriteria(User.class).setFetchMode("tagging",  FetchMode.JOIN);
		List<User> results = cr.list();
		return results;
	}
	
	
	
	@Override
	@Transactional
	public List<Role> getRoleList() throws Exception {
		// TODO Auto-generated method stub
		Session session = sessionFactory.getCurrentSession();
		Criteria cr = session.createCriteria(Role.class);
		List<Role> results = cr.list();
		return results;
	}

	
	@Override
	@Transactional
	public void saveRole(Role role) throws Exception {
		// Acquire session
		Session session = sessionFactory.getCurrentSession();
		// Save employee, saving behavior get done in a transactional manner
		session.saveOrUpdate(role);		
	}
	
	
	@Override
	@Transactional
	public void deleteUser(User user) throws Exception {
		// Acquire session
		Session session = sessionFactory.getCurrentSession();
		// Save employee, saving behavior get done in a transactional manner
		session.delete(user);		
	}
	
	@Override
	@Transactional
	public void deleteRole(Role role) throws Exception {
		// Acquire session
		Session session = sessionFactory.getCurrentSession();
		// Save employee, saving behavior get done in a transactional manner
		session.delete(role);		
	}
	
	
	@Override
	@Transactional
	public List<Tagging> getTaggingList() throws Exception {
		// TODO Auto-generated method stub
		Session session = sessionFactory.getCurrentSession();
		Criteria cr = session.createCriteria(Tagging.class);
		List<Tagging> results = cr.list();
		return results;
	}
	
	
	@Override
	@Transactional
	public void saveTagging(Tagging tag) throws Exception {
		// Acquire session
		Session session = sessionFactory.getCurrentSession();
		// Save employee, saving behavior get done in a transactional manner
		session.saveOrUpdate(tag);		
	}

	
	
	@Override
	@Transactional
	public void deleteTagging(Tagging tag) throws Exception {
		// Acquire session
		Session session = sessionFactory.getCurrentSession();
		// Save employee, saving behavior get done in a transactional manner
		session.delete(tag);		
	}
	
	
	
}
