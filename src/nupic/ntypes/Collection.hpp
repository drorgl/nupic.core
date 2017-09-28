/* ---------------------------------------------------------------------
 * Numenta Platform for Intelligent Computing (NuPIC)
 * Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
 * with Numenta, Inc., for a separate license for this software code, the
 * following terms and conditions apply:
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero Public License version 3 as
 * published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU Affero Public License for more details.
 *
 * You should have received a copy of the GNU Affero Public License
 * along with this program.  If not, see http://www.gnu.org/licenses.
 *
 * http://numenta.org/licenses/
 * ---------------------------------------------------------------------
 */

#ifndef NTA_COLLECTION_HPP
#define NTA_COLLECTION_HPP

#include <nupic/ntypes/Collection.hpp>
#include <nupic/utils/Log.hpp>
#include <string>
#include <vector>

namespace nupic
{
  // A collection is a templated class that contains items of type t.
  // It supports lookup by name and by index. The items are stored in a map
  // and copies are also stored in a vector (it's Ok to use pointers).
  // You can add items using the add() method.
  //
  template <typename T>
  class Collection
  {
  public:
	  Collection() {}
	virtual ~Collection() {}
    
    size_t getCount() const {
		return vec_.size();
	}

    // This method provides access by index to the contents of the collection
    // The indices are in insertion order.
    //

    const std::pair<std::string, T>& getByIndex(size_t index) const {
		NTA_CHECK(index < vec_.size());
		return vec_[index];
	}

	std::pair<std::string, T>& getByIndex(size_t index)
	{
		NTA_CHECK(index < vec_.size());
		return vec_[index];
	}

  
	bool contains(const std::string & name) const {
		typename CollectionStorage::const_iterator i;
		for (i = vec_.begin(); i != vec_.end(); i++)
		{
			if (i->first == name)
				return true;
		}
		return false;
	}

    T getByName(const std::string & name) const {
		typename CollectionStorage::const_iterator i;
		for (i = vec_.begin(); i != vec_.end(); i++)
		{
			if (i->first == name)
				return i->second;
		}
		NTA_THROW << "No item named: " << name;
	}

    // TODO: move add/remove to a ModifiableCollection subclass
    // This method should be internal but is currently tested
    // in net_test.py in test_node_spec
    void add(const std::string & name, const T & item) {
		// make sure we don't already have something with this name
		typename CollectionStorage::const_iterator i;
		for (i = vec_.begin(); i != vec_.end(); i++)
		{
			if (i->first == name)
			{
				NTA_THROW << "Unable to add item '" << name << "' to collection "
					<< "because it already exists";
		}
	}

		// Add the new item to the vector
		vec_.push_back(std::make_pair(name, item));
  }

    void remove(const std::string& name) {
		typename CollectionStorage::iterator i;
		for (i = vec_.begin(); i != vec_.end(); i++)
		{
			if (i->first == name)
				break;
	}
		if (i == vec_.end())
			NTA_THROW << "No item named '" << name << "' in collection";

		vec_.erase(i);
  }


//#ifdef NTA_INTERNAL
//    std::pair<std::string, T>& getByIndex(size_t index);
//#endif

  private:
    typedef std::vector<std::pair<std::string, T> > CollectionStorage;
    CollectionStorage vec_; 
  };
}

#endif

