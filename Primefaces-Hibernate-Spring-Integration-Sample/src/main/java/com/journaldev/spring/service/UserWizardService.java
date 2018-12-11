package com.journaldev.spring.service;

import java.util.List;

import com.journaldev.hibernate.entity.User;

public interface UserWizardService {

	public void register(User user) throws Exception;

	public List<User> getUsersList() throws Exception;
	

}
