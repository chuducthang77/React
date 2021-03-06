import { useState, useEffect } from "react";
import List from "./List";
import Alert from "./Alert";
import "./App.css";

const getLocalStorage = () => {
  let list = localStorage.getItem("list");
  if (list) {
    return JSON.parse(localStorage.getItem("list"));
  } else {
    return [];
  }
};

function App() {
  //Set up the state for the app

  const [name, setName] = useState("");
  const [list, setList] = useState(getLocalStorage());
  const [isEditing, setIsEditing] = useState(false);
  const [editID, setEditID] = useState(null);
  const [alert, setAlert] = useState({
    show: true,
    msg: "Welcome to the shopping list",
    type: "success",
  });
  const [addition, setAddition] = useState(true);
  const [finish, setFinish] = useState('Finish!')

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name) {
      showAlert(true, "danger", "please enter value");
    } else if (name && isEditing) {
      //Deal with edit
      setList(
        list.map((item) => {
          if (item.id === editID) {
            return { ...item, title: name };
          }
          return item;
        })
      );
      setName("");
      setEditID(null);
      setIsEditing(false);
      showAlert(true, "success", "Successful Update");
    } else {
      //Add to the list
      //Check whether the item has been added to the list
      const check = list.find((item) => item.title.toLowerCase() === name.toLowerCase())
      if (!check || list.length === 0) {
        showAlert(true, "success", `${name} added to the list`);
        const newItem = { id: new Date().getTime().toString(), title: name };
        setList([...list, newItem]);
        setName("");
      } else {
        showAlert(true, 'danger', 'Item has been added')
        setName("")
      }
      
    }
  };

  const showAlert = (show = false, type = "", msg = "") => {
    setAlert({ show, type, msg });
  };

  const clearList = () => {
    showAlert(true, "danger", "empty list");
    setList([]);
  };

  const removeItem = (id) => {
    showAlert(true, "danger", "Item removed");
    //Remove the item from the list
    setList(list.filter((item) => item.id !== id));
  };

  const editItem = (id) => {
    const specificItem = list.find((item) => item.id === id);
    setIsEditing(true);
    setEditID(id);
    setName(specificItem.title);
  };

  const clearAddition = () => {
    setAddition(false);
    setFinish('List of item')
  };

  useEffect(() => {
    localStorage.setItem("list", JSON.stringify(list));
  }, [list]);

  return (
    <section className="section-center">
      {addition && (
        <form className="grocery-form" onSubmit={handleSubmit}>
          {/* Show the alert when the delete 
        Note: ...alert means pass all the property
        Note: the list */}
          {alert.show && (
            <Alert {...alert} removeAlert={showAlert} list={list} />
          )}
          <h3>Shopping List</h3>
          <div className="from-control">
            {/* Let the user type in the grocery */}
            <input
              type="text"
              className="grocery"
              placeholder="eg. eggs"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            {/* Edit or Submit button */}
            <button type="submit" className="submit-btn">
              {isEditing ? "edit" : "submit"}
            </button>
          </div>
        </form>
      )}

      {/* Grocery container */}
      {list.length > 0 && addition && (
        <div className="grocery-container">
          <List items={list} removeItem={removeItem} editItem={editItem} />
          <button className="clear-btn" onClick={clearList}>
            Clear items
          </button>
        </div>
      )}

      {/* New Implementation: Allow user to Finish the shopping list, display the list, where to buy them,  */}
      {list.length > 0 && (
        <div className="grocery-container">
          <button className="finish-btn" onClick={clearAddition}>
            {finish}
          </button>
        </div>
      )}

      {/* Display the final list */}
      {/* Do not allow the user to edit or delete the items */}
      {!addition && (<List items={list}/>)}
    </section>
  );
}

export default App;
