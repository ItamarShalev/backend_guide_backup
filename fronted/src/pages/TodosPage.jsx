import { useState } from 'react';
import { useTodos } from '../hooks/useTodos';
import TodoCard from '../components/TodoCard';
import './TodosPage.css';

const TodosPage = () => {
  const { todos, loading, error, createTodo, updateTodo, deleteTodo, fetchTodos } = useTodos();
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState('all');
  const [newTodo, setNewTodo] = useState({ title: '', description: '' });

  const handleCreateTodo = async (e) => {
    e.preventDefault();
    const result = await createTodo(newTodo);
    if (result.success) {
      setNewTodo({ title: '', description: '' });
      setShowForm(false);
    }
  };

  const handleFilterChange = (newFilter) => {
    setFilter(newFilter);
    const completed = newFilter === 'all' ? null : newFilter === 'completed';
    fetchTodos(completed);
  };

  const filteredTodos = todos;

  if (loading) {
    return (
      <div className="todos-page">
        <div className="loading">Loading your todos...</div>
      </div>
    );
  }

  return (
    <div className="todos-page">
      <div className="todos-header">
        <h1>My Todos</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="add-todo-btn"
        >
          {showForm ? 'Cancel' : 'Add Todo'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {showForm && (
        <div className="todo-form-container">
          <form onSubmit={handleCreateTodo} className="todo-form">
            <input
              type="text"
              placeholder="Todo title"
              value={newTodo.title}
              onChange={(e) => setNewTodo({...newTodo, title: e.target.value})}
              required
            />
            <textarea
              placeholder="Description (optional)"
              value={newTodo.description}
              onChange={(e) => setNewTodo({...newTodo, description: e.target.value})}
              rows="3"
            />
            <button type="submit">Create Todo</button>
          </form>
        </div>
      )}

      <div className="filter-tabs">
        <button
          onClick={() => handleFilterChange('all')}
          className={filter === 'all' ? 'active' : ''}
        >
          All ({todos.length})
        </button>
        <button
          onClick={() => handleFilterChange('pending')}
          className={filter === 'pending' ? 'active' : ''}
        >
          Pending ({todos.filter(t => !t.completed).length})
        </button>
        <button
          onClick={() => handleFilterChange('completed')}
          className={filter === 'completed' ? 'active' : ''}
        >
          Completed ({todos.filter(t => t.completed).length})
        </button>
      </div>

      <div className="todos-list">
        {filteredTodos.length === 0 ? (
          <div className="empty-state">
            <p>No todos found.</p>
            <p>Create your first todo to get started!</p>
          </div>
        ) : (
          filteredTodos.map((todo) => (
            <TodoCard
              key={todo.id}
              todo={todo}
              onUpdate={updateTodo}
              onDelete={deleteTodo}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default TodosPage;
