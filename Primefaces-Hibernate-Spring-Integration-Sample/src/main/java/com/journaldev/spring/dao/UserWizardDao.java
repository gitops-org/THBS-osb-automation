package com.journaldev.spring.dao;

import java.util.List;

import com.journaldev.hibernate.entity.User;

public interface UserWizardDao {
	
	public void register(User user) throws Exception;

	public List<User> getUserList() throws Exception;

}
