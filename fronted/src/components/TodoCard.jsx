import { useState } from 'react';
import './TodoCard.css';

const TodoCard = ({ todo, onUpdate, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({
    title: todo.title,
    description: todo.description,
    completed: todo.completed,
  });

  const handleSave = async () => {
    const result = await onUpdate(todo.id, editData);
    if (result.success) {
      setIsEditing(false);
    }
  };

  const handleToggleComplete = async () => {
    await onUpdate(todo.id, { ...todo, completed: !todo.completed });
  };

  return (
    <div className={`todo-card ${todo.completed ? 'completed' : ''}`}>
      {isEditing ? (
        <div className="edit-form">
          <input
            type="text"
            value={editData.title}
            onChange={(e) => setEditData({...editData, title: e.target.value})}
            className="edit-title"
            placeholder="Todo title"
          />
          <textarea
            value={editData.description}
            onChange={(e) => setEditData({...editData, description: e.target.value})}
            className="edit-description"
            placeholder="Description"
            rows="3"
          />
          <div className="edit-actions">
            <button onClick={handleSave} className="save-btn">Save</button>
            <button onClick={() => setIsEditing(false)} className="cancel-btn">Cancel</button>
          </div>
        </div>
      ) : (
        <>
          <div className="todo-content">
            <h3 className="todo-title">{todo.title}</h3>
            {todo.description && (
              <p className="todo-description">{todo.description}</p>
            )}
          </div>
          <div className="todo-actions">
            <button
              onClick={handleToggleComplete}
              className={`complete-btn ${todo.completed ? 'completed' : ''}`}
            >
              {todo.completed ? '✓' : '○'}
            </button>
            <button onClick={() => setIsEditing(true)} className="edit-btn">
              ✏️
            </button>
            <button onClick={() => onDelete(todo.id)} className="delete-btn">
              🗑️
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default TodoCard;
