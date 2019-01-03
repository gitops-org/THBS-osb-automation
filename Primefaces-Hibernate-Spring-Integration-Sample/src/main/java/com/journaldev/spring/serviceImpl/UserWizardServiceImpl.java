package com.journaldev.spring.serviceImpl;

import java.util.List;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import com.journaldev.hibernate.entity.Role;
import com.journaldev.hibernate.entity.User;
import com.journaldev.spring.dao.UserWizardDao;
import com.journaldev.spring.service.UserWizardService;

@Service
public class UserWizardServiceImpl implements UserWizardService{
	
	
	@Autowired
	private SessionFactory sessionFactory;
	
	@Autowired
	private UserWizardDao userWizardDao;
	
	public UserWizardDao getUserWizardDao() {
		return userWizardDao;
	}

	public void setUserWizardDao(UserWizardDao userWizardDao) {
		this.userWizardDao = userWizardDao;
	}

	public SessionFactory getSessionFactory() {
		return sessionFactory;
	}

	public void setSessionFactory(SessionFactory sessionFactory) {
		this.sessionFactory = sessionFactory;
	}
	
	
	/* (non-Javadoc)
	 * @see com.journaldev.spring.service.UserWizardService#register(com.journaldev.hibernate.entity.User)
	 */
	@Override
	public void register(User user) throws Exception{
		userWizardDao.register(user);
	}

	/* (non-Javadoc)
	 * @see com.journaldev.spring.service.UserWizardService#getUsersList()
	 */
	@Override
	public List<User> getUsersList() throws Exception {
		// TODO Auto-generated method stub
		List<User> userList = userWizardDao.getUserList();
		return userList;
	}

	@Override
	public List<Role> getRoleList() throws Exception {
		// TODO Auto-generated method stub
		List<Role> roleList = userWizardDao.getRoleList();
		return roleList;
	}
	
	/* (non-Javadoc)
	 * @see com.journaldev.spring.service.UserWizardService#register(com.journaldev.hibernate.entity.User)
	 */
	@Override
	public void saveRole(Role role) throws Exception{
		userWizardDao.saveRole(role);
	}
	
	
	/* (non-Javadoc)
	 * @see com.journaldev.spring.service.UserWizardService#register(com.journaldev.hibernate.entity.User)
	 */
	@Override
	public void deleteUser(User user) throws Exception{
		userWizardDao.deleteUser(user);
	}

	
	/* (non-Javadoc)
	 * @see com.journaldev.spring.service.UserWizardService#register(com.journaldev.hibernate.entity.User)
	 */
	@Override
	public void deleteRole(Role role) throws Exception{
		userWizardDao.deleteRole(role);
	}


}