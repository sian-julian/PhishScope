import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, LineChart, Line, CartesianGrid
} from 'recharts';
import StatsCard from '../components/StatsCard';
import ChartCard from '../components/ChartCard';

const Dashboard = () => {
  // Mock Data as per prompt instructions
  const stats = {
    total: 150,
    safe: 120,
    suspicious: 10,
    dangerous: 20,
    avgConfidence: "96.4%"
  };

  const pieData = [
    { name: 'Safe', value: stats.safe, color: '#22C55E' },
    { name: 'Suspicious', value: stats.suspicious, color: '#EAB308' },
    { name: 'Dangerous', value: stats.dangerous, color: '#EF4444' },
  ];

  const featureData = [
    { name: 'Lookalike', impact: 85 },
    { name: 'Entropy', impact: 65 },
    { name: 'Suspicious TLD', impact: 45 },
    { name: 'Brand Mismatch', impact: 40 },
  ];

  const lineData = [
    { day: 'Mon', analyzed: 12 },
    { day: 'Tue', analyzed: 19 },
    { day: 'Wed', analyzed: 15 },
    { day: 'Thu', analyzed: 25 },
    { day: 'Fri', analyzed: 22 },
    { day: 'Sat', analyzed: 40 },
    { day: 'Sun', analyzed: 17 },
  ];

  return (
    <div className="flex flex-col w-full max-w-7xl mx-auto py-8 space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold mb-2">Global Dashboard</h1>
        <p className="text-gray-400">Real-time statistics from the PhishScope Hybrid Engine.</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <StatsCard title="Total URLs" value={stats.total} colorClass="border-blue-500" />
        <StatsCard title="Safe" value={stats.safe} colorClass="border-green-500" />
        <StatsCard title="Suspicious" value={stats.suspicious} colorClass="border-yellow-500" />
        <StatsCard title="Dangerous" value={stats.dangerous} colorClass="border-red-500" />
        <StatsCard title="Avg Confidence" value={stats.avgConfidence} colorClass="border-purple-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <ChartCard title="Safe vs Dangerous Distribution">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#fff' }}
                itemStyle={{ color: '#fff' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Top Global Phishing Indicators">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={featureData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <XAxis type="number" hide />
              <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{fill: '#9CA3AF'}} width={120} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#fff' }}
                cursor={{fill: 'rgba(255,255,255,0.05)'}}
              />
              <Bar dataKey="impact" fill="#EF4444" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="URLs Analyzed (7 Days)">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={lineData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
              <XAxis dataKey="day" stroke="#9CA3AF" tickLine={false} />
              <YAxis stroke="#9CA3AF" tickLine={false} axisLine={false} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#fff' }}
              />
              <Line type="monotone" dataKey="analyzed" stroke="#2563EB" strokeWidth={3} dot={{r: 4, fill: '#2563EB'}} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </div>
  );
};

export default Dashboard;
