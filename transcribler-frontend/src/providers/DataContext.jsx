import React, { createContext, useState, useContext, useEffect } from 'react';

const DataContext = createContext(undefined);

export const DataProvider = ({ children }) => {
  const [data, setData] = useState(null);
  const [currentUrl, setCurrentUrl] = useState(window.location.href);

  useEffect(() => {
    const handleUrlChange = () => {
      setCurrentUrl(window.location.href);
    };

    window.addEventListener('popstate', handleUrlChange);
    window.addEventListener('pushState', handleUrlChange);
    window.addEventListener('replaceState', handleUrlChange);

    return () => {
      window.removeEventListener('popstate', handleUrlChange);
      window.removeEventListener('pushState', handleUrlChange);
      window.removeEventListener('replaceState', handleUrlChange);
    };
  }, []);

  return (
    <DataContext.Provider value={{ data, setData, currentUrl }}>
      {children}
    </DataContext.Provider>
  );
}

export const useData = () => {
  const context = useContext(DataContext);
  if (context === undefined) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
}