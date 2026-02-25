import React, { useState } from 'react';
import {
  BarChart3,
  Truck,
  Package,
  Users,
  LayoutDashboard,
  Settings,
  Bell,
  Search,
  ArrowUpRight,
  ArrowDownRight,
  TrendingUp,
  Clock,
  MapPin
} from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Line, Doughnut, Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const renderSubtitle = (tab) => {
  switch (tab) {
    case 'dashboard': return 'Real-time optimization engine status';
    case 'inventory': return 'Global SKU distribution and stock health';
    case 'shipments': return 'In-transit visibility and route efficiency';
    case 'suppliers': return 'Vendor performance and compliance metrics';
    case 'analytics': return 'Deep-dive forecasting and risk modeling';
    default: return 'Supply Chain Optimization System';
  }
};

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const PAGE_SIZE = 50;
  const [stats, setStats] = useState({
    totalShipments: "---",
    avgLeadTime: "---",
    totalCost: "---",
    warehouseDist: {},
    lastUpdated: "Never",
    monthlyTrends: Array(12).fill(0),
    warehouseCapacity: [],
    topCategories: { labels: [], data: [] },
    recentShipments: [],
    supplierStats: []
  });

  React.useEffect(() => {
    fetch('/stats.json')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.log("Stats not yet generated"));
  }, []);

  // Multi-line chart data (Shipment Trends)
  const lineData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [
      {
        label: 'Monthly Shipments',
        data: stats.monthlyTrends,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4,
      }
    ],
  };

  // Inventory distribution from real data
  const doughnutData = {
    labels: Object.keys(stats.warehouseDist),
    datasets: [{
      data: Object.values(stats.warehouseDist),
      backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#6366f1', '#f43f5e'],
      borderWidth: 0,
    }]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#1c2633',
        titleFont: { family: 'Outfit', size: 14 },
        bodyFont: { family: 'Inter', size: 12 },
        padding: 12,
        cornerRadius: 10,
      }
    },
    scales: {
      x: { grid: { display: false }, ticks: { color: '#64748b' } },
      y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } }
    }
  };

  const filteredShipments = stats.recentShipments.filter(ship =>
    ship.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    ship.origin.toLowerCase().includes(searchQuery.toLowerCase()) ||
    ship.product.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const paginatedShipments = filteredShipments.slice(
    (currentPage - 1) * PAGE_SIZE,
    currentPage * PAGE_SIZE
  );

  const totalPages = Math.ceil(filteredShipments.length / PAGE_SIZE);

  React.useEffect(() => {
    setCurrentPage(1);
  }, [searchQuery]);

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">SC_OPTIMIZE</div>
        <nav>
          <a href="#" className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
            <LayoutDashboard /> Dashboard
          </a>
          <a href="#" className={`nav-link ${activeTab === 'inventory' ? 'active' : ''}`} onClick={() => setActiveTab('inventory')}>
            <Package /> Inventory
          </a>
          <a href="#" className={`nav-link ${activeTab === 'shipments' ? 'active' : ''}`} onClick={() => setActiveTab('shipments')}>
            <Truck /> Shipments
          </a>
          <a href="#" className={`nav-link ${activeTab === 'suppliers' ? 'active' : ''}`} onClick={() => setActiveTab('suppliers')}>
            <Users /> Suppliers
          </a>
          <a href="#" className={`nav-link ${activeTab === 'analytics' ? 'active' : ''}`} onClick={() => setActiveTab('analytics')}>
            <BarChart3 /> Analytics
          </a>
        </nav>
        <div style={{ marginTop: 'auto' }}>
          <a href="#" className="nav-link"><Settings /> Settings</a>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="header">
          <div className="title-section">
            <h1>{activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Overview</h1>
            <p>{renderSubtitle(activeTab)}</p>
          </div>
          <div className="user-section" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <div className="search-bar" style={{ background: 'var(--bg-secondary)', padding: '0.5rem 1rem', borderRadius: '10px', display: 'flex', alignItems: 'center', border: '1px solid var(--glass-border)' }}>
              <Search size={18} color="#64748b" />
              <input type="text" placeholder="Search data..." style={{ background: 'none', border: 'none', outline: 'none', marginLeft: '0.5rem', color: 'white' }} />
            </div>
            <div className="icon-btn" style={{ background: 'var(--bg-secondary)', padding: '0.5rem', borderRadius: '10px', border: '1px solid var(--glass-border)', cursor: 'pointer' }}>
              <Bell size={20} />
            </div>
          </div>
        </header>

        {activeTab === 'dashboard' && (
          <>
            <div className="stats-grid">
              <StatCard icon={<Truck />} label="Total Shipments" value={stats.totalShipments} trend="+12.5%" isUp={true} />
              <StatCard icon={<Clock />} label="Avg. Lead Time" value={stats.avgLeadTime} trend="OPTIMIZED" isUp={true} />
              <StatCard icon={<TrendingUp />} label="Total Logistics Cost" value={stats.totalCost} trend="STABLE" isUp={true} />
              <StatCard icon={<Search />} label="Last ETL Sync" value={stats.lastUpdated} trend="LIVE" isUp={true} />
            </div>

            <div className="charts-grid">
              <div className="chart-card">
                <div className="chart-header">
                  <h3>Shipment Velocity</h3>
                </div>
                <div style={{ height: '300px' }}>
                  <Line data={lineData} options={chartOptions} />
                </div>
              </div>
              <div className="chart-card">
                <div className="chart-header">
                  <h3>Distribution by Hub</h3>
                </div>
                <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Doughnut data={doughnutData} options={{ ...chartOptions, scales: {} }} />
                </div>
              </div>
            </div>

            <div className="table-card">
              <div className="chart-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3>Recent Active Shipments</h3>
                <button
                  onClick={() => setActiveTab('shipments')}
                  style={{ background: 'var(--accent-primary)', border: 'none', color: 'white', padding: '0.5rem 1rem', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}
                >
                  View All
                </button>
              </div>
              <table>
                <thead>
                  <tr>
                    <th>Shipment ID</th>
                    <th>Product</th>
                    <th>Origin</th>
                    <th>Destination</th>
                    <th>Status</th>
                    <th>Efficiency</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.recentShipments.slice(0, 4).map(ship => (
                    <TableRow key={ship.id} {...ship} />
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}

        {activeTab === 'inventory' && (
          <div className="charts-grid" style={{ gridTemplateColumns: '1fr' }}>
            <div className="chart-card">
              <h3>Warehouse Capacity Utilization</h3>
              <div style={{ marginTop: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                {stats.warehouseCapacity.map(wh => (
                  <CapacityBar key={wh.id} name={wh.name} usage={wh.usage} color={wh.usage > 90 ? "#ef4444" : "#3b82f6"} />
                ))}
              </div>
            </div>
            <div className="table-card">
              <h3>Top Stocked Categories</h3>
              <div style={{ height: '300px', marginTop: '1rem' }}>
                <Bar
                  data={{
                    labels: stats.topCategories.labels,
                    datasets: [{
                      label: 'Units in Stock',
                      data: stats.topCategories.data,
                      backgroundColor: 'rgba(99, 102, 241, 0.5)',
                      borderColor: '#6366f1',
                      borderWidth: 2
                    }]
                  }}
                  options={chartOptions}
                />
              </div>
            </div>
          </div>
        )}

        {activeTab === 'shipments' && (
          <div className="table-card" style={{ marginTop: '0' }}>
            <div className="chart-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <div>
                <h3>Global Shipment Registry</h3>
                <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                  Showing latest {stats.recentShipments.length} records of {stats.totalShipments} processed
                  {stats.totalRecordsRaw > 1000 && " (Truncated for performance)"}
                </p>
              </div>
              <div className="search-bar" style={{ background: 'var(--bg-secondary)', padding: '0.5rem 1rem', borderRadius: '10px', display: 'flex', alignItems: 'center', border: '1px solid var(--glass-border)', width: '300px' }}>
                <Search size={18} color="#64748b" />
                <input
                  type="text"
                  placeholder="Filter by ID, Origin, Product..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  style={{ background: 'none', border: 'none', outline: 'none', marginLeft: '0.5rem', color: 'white', width: '100%' }}
                />
              </div>
            </div>
            <table>
              <thead>
                <tr>
                  <th>Shipment ID</th>
                  <th>Product</th>
                  <th>Current Location</th>
                  <th>Status</th>
                  <th>Efficiency</th>
                </tr>
              </thead>
              <tbody>
                {paginatedShipments.map(ship => (
                  <TableRow key={ship.id} {...ship} />
                ))}
              </tbody>
            </table>

            {/* Pagination Controls */}
            {totalPages > 1 && (
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1.5rem', paddingTop: '1rem', borderTop: '1px solid var(--glass-border)' }}>
                <div style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
                  Page {currentPage} of {totalPages} ({filteredShipments.length} total found)
                </div>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button
                    disabled={currentPage === 1}
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    style={{ background: 'var(--bg-secondary)', border: '1px solid var(--glass-border)', color: 'white', padding: '0.5rem 1rem', borderRadius: '6px', cursor: currentPage === 1 ? 'not-allowed' : 'pointer', opacity: currentPage === 1 ? 0.5 : 1 }}
                  >
                    Previous
                  </button>
                  <button
                    disabled={currentPage === totalPages}
                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    style={{ background: 'var(--accent-primary)', border: 'none', color: 'white', padding: '0.5rem 1rem', borderRadius: '6px', cursor: currentPage === totalPages ? 'not-allowed' : 'pointer', opacity: currentPage === totalPages ? 0.5 : 1 }}
                  >
                    Next 50
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'suppliers' && (
          <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))' }}>
            {stats.supplierStats.map(sup => (
              <SupplierCard key={sup.name} {...sup} />
            ))}
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="charts-grid" style={{ gridTemplateColumns: '1fr' }}>
            <div className="chart-card">
              <h3>Lead Time Forecast (Projected vs Actual)</h3>
              <div style={{ height: '400px' }}>
                <Line
                  data={{
                    labels: ['Q1', 'Q2', 'Q3', 'Q4', 'Q1-P', 'Q2-P'],
                    datasets: [
                      {
                        label: 'Actual Days',
                        data: [22, 25, 28, 24, null, null],
                        borderColor: '#10b981',
                        tension: 0.4
                      },
                      {
                        label: 'Projected Days',
                        data: [22, 24, 26, 23, 22, 21],
                        borderColor: '#3b82f6',
                        borderDash: [5, 5],
                        tension: 0.4
                      }
                    ]
                  }}
                  options={chartOptions}
                />
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

const CapacityBar = ({ name, usage, color }) => (
  <div style={{ width: '100%' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
      <span style={{ fontWeight: '500' }}>{name}</span>
      <span style={{ color: usage > 90 ? '#ef4444' : 'inherit' }}>{usage}%</span>
    </div>
    <div style={{ height: '8px', background: 'var(--bg-secondary)', borderRadius: '4px', overflow: 'hidden' }}>
      <div style={{ height: '100%', width: `${usage}%`, background: color, transition: 'width 1s ease-out' }} />
    </div>
  </div>
);

const SupplierCard = ({ name, country, rating, shipments }) => (
  <div className="stat-card" style={{ padding: '1.5rem' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
      <div style={{ width: '40px', height: '40px', background: 'var(--bg-tertiary)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Users size={20} />
      </div>
      <div style={{ background: '#10b98122', color: '#10b981', padding: '0.2rem 0.6rem', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold' }}>
        ★ {rating}
      </div>
    </div>
    <h4 style={{ margin: '0 0 0.25rem 0' }}>{name}</h4>
    <div style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '1rem' }}>{country}</div>
    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', borderTop: '1px solid var(--glass-border)', paddingTop: '1rem' }}>
      <span style={{ color: 'var(--text-secondary)' }}>Total Shipments</span>
      <span style={{ fontWeight: 'bold' }}>{shipments}</span>
    </div>
  </div>
);

const StatCard = ({ icon, label, value, trend, isUp }) => (
  <div className="stat-card">
    <div className="stat-header">
      <div className="stat-icon">{icon}</div>
      <div className={`stat-trend ${isUp ? 'trend-up' : 'trend-down'}`}>
        {isUp ? <ArrowUpRight size={16} /> : <ArrowDownRight size={16} />}
        {trend}
      </div>
    </div>
    <div className="stat-label">{label}</div>
    <div className="stat-value">{value}</div>
  </div>
);

const TableRow = ({ id, product, origin, dest, status, efficiency }) => (
  <tr>
    <td><span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{id}</span></td>
    <td>{product}</td>
    <td><div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><MapPin size={14} /> {origin}</div></td>
    <td><div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><MapPin size={14} /> {dest}</div></td>
    <td>
      <span className={`status-badge status-${status.toLowerCase()}`}>
        {status}
      </span>
    </td>
    <td>{efficiency}</td>
  </tr>
);

export default App;
