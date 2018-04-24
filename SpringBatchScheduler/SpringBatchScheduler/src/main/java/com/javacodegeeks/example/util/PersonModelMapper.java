package com.javacodegeeks.example.util;

import java.sql.ResultSet;
import java.sql.SQLException;

import org.springframework.jdbc.core.RowMapper;

public class PersonModelMapper implements RowMapper<PersonModel>{

	public PersonModel mapRow(ResultSet rs, int rowNum) throws SQLException {
		PersonModel person = new PersonModel();
		person.setFirstName(rs.getString("firstName"));
		person.setLastName(rs.getString("lastName"));
		person.setSchool(rs.getString("school"));
		person.setRollNumber(rs.getInt("rollNumber"));
		return person;
	}

}
