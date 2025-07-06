import { useState, useEffect, useCallback } from 'react';
import ApiService from '../services/api';

export const useTodos = () => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTodos = useCallback(async (completed = null) => {
    try {
      setLoading(true);
      setError(null);
      const data = await ApiService.getTodos(completed);
      setTodos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const createTodo = async (todoData) => {
    try {
      const newTodo = await ApiService.createTodo(todoData);
      setTodos(prev => [newTodo, ...prev]);
      return { success: true };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  const updateTodo = async (todoId, todoData) => {
    try {
      const updatedTodo = await ApiService.updateTodo(todoId, todoData);
      setTodos(prev => prev.map(todo => 
        todo.id === todoId ? updatedTodo : todo
      ));
      return { success: true };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  const deleteTodo = async (todoId) => {
    try {
      await ApiService.deleteTodo(todoId);
      setTodos(prev => prev.filter(todo => todo.id !== todoId));
      return { success: true };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  return {
    todos,
    loading,
    error,
    fetchTodos,
    createTodo,
    updateTodo,
    deleteTodo,
  };
};
