from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from lightMed.database.database import Base, ma
from marshmallow import fields, post_load
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Location(Base):
    __tablename__ = 'locations'

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String)
    city_id = Column(Integer, ForeignKey("cities.city_id"), autoincrement=True)
    visit = relationship("VisitToLocation", back_populates="location")
    booked_visit = relationship("Visit", back_populates="location")
    city = relationship("City", back_populates="locations")

    def __repr__(self):
        return "<Location(location_id='%s', address='%s')>" % (self.location_id, self.address)

class City(Base):
    __tablename__ = "cities"

    city_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    locations = relationship("Location", back_populates="city")

class VisitToLocation(Base):
    __tablename__ = 'visit_to_location'

    visit_to_location_id = Column(Integer, primary_key=True, autoincrement=True) 
    visit_id = Column(Integer, ForeignKey('visits.visit_id'), autoincrement=True)
    location_id = Column(Integer, ForeignKey('locations.location_id'), autoincrement=True)
    location = relationship("Location", back_populates="visit")
    visit = relationship("Visit", back_populates="locations")
    

    def __repr__(self):
        return ("<VisitToLocation(visit_to_location.visit_id='%s', visit_to_location.location_id='%s')>" 
                % (self.visit_id, self.location_id))


class Specialization(Base):
    __tablename__ = 'specializations'

    specialization_id = Column(Integer, primary_key=True, autoincrement=True)
    specialization = Column(String)
    visit = relationship("Visit", back_populates="specialization")

    def __repr__(self):
        return "<Specialization(specialization_id='%s', specialization='%s')>" % (self.specialization_id, self.specialization)


class Visit(Base):
    __tablename__ = 'visits'

    visit_id = Column(Integer, primary_key=True, autoincrement=True)
    specialization_id = Column(Integer, ForeignKey('specializations.specialization_id'), autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), autoincrement=True)
    after_date = Column(String)
    booked_date_time = Column(String)
    booked_location = Column(Integer, ForeignKey('locations.location_id'), autoincrement=True)

    specialization = relationship("Specialization", back_populates="visit")
    locations = relationship("VisitToLocation", back_populates="visit", cascade="all, delete")
    time_frames = relationship("TimeFrame", back_populates="visit", cascade="all, delete")
    user = relationship("User", back_populates="visits")
    location = relationship("Location", back_populates="booked_visit")

    def __repr__(self):
        return ("<Visit(visit_id='%s', specialization_id='%s', after_date='%s', booked_date_time='%s', user='%s', locations='%s')>"
                     % (self.visit_id, self.specialization_id, self.after_date, self.booked_date_time, self.user, self.locations))


class TimeFrame(Base):
    __tablename__ = 'time_frames'

    time_frame_id = Column(Integer, primary_key=True, autoincrement=True)
    visit_id = Column(Integer, ForeignKey('visits.visit_id'), autoincrement=True)
    start_time = Column(String)
    end_time = Column(String)
    visit = relationship("Visit", back_populates="time_frames")

    def __repr__(self):
        return ("<time_frame(start_time='%s', end_time='%s')>"
                     % (self.start_time, self.end_time))

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String)
    user_password = Column(String)
    visits = relationship("Visit", back_populates="user")
    def __repr__(self):
        return ("<User(user_id='%s', user_name='%s')>"
                    % (self.user_id, self.user_name))


class TimeFrameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TimeFrame
    
    @post_load
    def make_time_frame(self, data, **kwargs):
        return TimeFrame(**data)


class SpecializationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Specialization

    @post_load
    def make_specialization(self, data, **kwargs):
        return Specialization(**data)


class VisitToLocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VisitToLocation
        include_fk = True

    @post_load
    def make_visit_to_location(self, data, **kwargs):
        return VisitToLocation(**data)

class LocationSchemaSimple(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location

class CitySchema(ma.SQLAlchemyAutoSchema):
    #name = fields.String()
    locations = fields.List(fields.Nested(LocationSchemaSimple(exclude=("location_id",))))
    class Meta:
        model = City


class LocationSchema(ma.SQLAlchemyAutoSchema):
    city_name = fields.Pluck(CitySchema, "name", attribute="city")
    class Meta:
        model = Location




class VisitToLocationSchemaForVisits(ma.SQLAlchemyAutoSchema):
    location = fields.Nested(LocationSchema)    


class UserSchema(ma.SQLAlchemyAutoSchema):
    user_id = fields.Int(dump_only=True)
    user_name = fields.String()
    user_password = fields.String()


class UserSchemaSimple(ma.SQLAlchemyAutoSchema):
    user_name = fields.String()
    user_id = fields.Int()


class VisitSchema(ma.SQLAlchemyAutoSchema):
    booked_location = fields.Nested(LocationSchema, attribute="location")
    specialization = fields.Nested(SpecializationSchema)
    locations = fields.Pluck(VisitToLocationSchemaForVisits, "location", many=True)
    time_frames = fields.Nested(TimeFrameSchema, many=True)
    user = fields.Nested(UserSchemaSimple)
    class Meta:
        model = Visit
