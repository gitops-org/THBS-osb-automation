package com.journaldev.spring.dao;

import java.util.List;

import com.journaldev.hibernate.entity.Role;
import com.journaldev.hibernate.entity.Tagging;
import com.journaldev.hibernate.entity.User;

public interface UserWizardDao {
	
	public void register(User user) throws Exception;

	public List<User> getUserList() throws Exception;
	
	public List<Role> getRoleList() throws Exception;
	
	public void saveRole(Role role) throws Exception;

	public void deleteUser(User user)throws Exception;

	public void deleteRole(Role role) throws Exception;

	public List<Tagging> getTaggingList()throws Exception;

	public void saveTagging(Tagging tag)throws Exception;

	public void deleteTagging(Tagging tag) throws Exception;

}
