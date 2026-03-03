
# 创建 OpenClaw Dashboard 的完整 HTML/CSS/JS 单页应用
# 采用 Cyberpunk/Command Center 风格设计

dashboard_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw Mission Control - 多智能体指挥面板</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary: #0066FF;
            --accent: #00D4FF;
            --success: #00FF88;
            --warning: #FFB800;
            --danger: #FF3366;
            --bg-dark: #0a0a0f;
            --bg-card: rgba(20, 20, 30, 0.8);
            --border: rgba(0, 212, 255, 0.2);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-dark);
            color: #e0e0e0;
            overflow-x: hidden;
        }
        
        .font-mono {
            font-family: 'JetBrains Mono', monospace;
        }
        
        /* Glassmorphism Cards */
        .glass-card {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 102, 255, 0.1);
        }
        
        .glass-card:hover {
            border-color: rgba(0, 212, 255, 0.4);
            box-shadow: 0 8px 32px rgba(0, 102, 255, 0.2);
        }
        
        /* Neon Glow Effects */
        .glow-text {
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        }
        
        .glow-border {
            box-shadow: 0 0 20px rgba(0, 102, 255, 0.3);
        }
        
        /* Status Indicators */
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            animation: pulse 2s infinite;
        }
        
        .status-active { background: var(--success); box-shadow: 0 0 10px var(--success); }
        .status-idle { background: var(--warning); box-shadow: 0 0 10px var(--warning); }
        .status-error { background: var(--danger); box-shadow: 0 0 10px var(--danger); }
        .status-offline { background: #666; }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Grid Background */
        .grid-bg {
            background-image: 
                linear-gradient(rgba(0, 102, 255, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 102, 255, 0.05) 1px, transparent 1px);
            background-size: 50px 50px;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(0, 212, 255, 0.3);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(0, 212, 255, 0.5);
        }
        
        /* Animations */
        @keyframes slideIn {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .animate-slide-in {
            animation: slideIn 0.3s ease-out;
        }
        
        .animate-fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        
        /* Terminal Effect */
        .terminal {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(0, 212, 255, 0.3);
            font-family: 'JetBrains Mono', monospace;
        }
        
        .terminal-line {
            padding: 2px 0;
            border-left: 3px solid transparent;
            padding-left: 8px;
        }
        
        .terminal-line:hover {
            background: rgba(0, 102, 255, 0.1);
            border-left-color: var(--accent);
        }
        
        /* Node Graph Styles */
        .node {
            position: absolute;
            width: 140px;
            padding: 12px;
            background: rgba(20, 20, 35, 0.95);
            border: 2px solid var(--primary);
            border-radius: 8px;
            cursor: move;
            transition: all 0.3s;
            z-index: 10;
        }
        
        .node:hover {
            transform: scale(1.05);
            box-shadow: 0 0 30px rgba(0, 102, 255, 0.4);
        }
        
        .node.selected {
            border-color: var(--accent);
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        }
        
        .connection {
            stroke: var(--primary);
            stroke-width: 2;
            fill: none;
            opacity: 0.6;
        }
        
        .connection.active {
            stroke: var(--accent);
            opacity: 1;
            stroke-dasharray: 5,5;
            animation: dash 1s linear infinite;
        }
        
        @keyframes dash {
            to { stroke-dashoffset: -10; }
        }
    </style>
</head>
<body class="grid-bg">
    <div id="root"></div>
    
    <script type="text/babel">
        const { useState, useEffect, useRef, useCallback } = React;
        
        // 模拟数据
        const mockAgents = [
            { id: 'supervisor', name: '总调度员(小小海)', role: 'Supervisor', status: 'active', tasks: 12, latency: '45ms', cpu: 23, memory: '456MB' },
            { id: 'memory', name: '记忆管理员', role: 'MemoryKeeper', status: 'active', tasks: 45, latency: '12ms', cpu: 15, memory: '1.2GB' },
            { id: 'quality', name: '质量检查员', role: 'QualityAssurance', status: 'idle', tasks: 0, latency: '-', cpu: 5, memory: '128MB' },
            { id: 'content', name: '自媒体运营者', role: 'ContentOperator', status: 'active', tasks: 3, latency: '234ms', cpu: 34, memory: '678MB' },
            { id: 'tech', name: '技术研究员', role: 'TechResearcher', status: 'active', tasks: 7, latency: '123ms', cpu: 28, memory: '890MB' },
            { id: 'life', name: '生活助手', role: 'LifeAssistant', status: 'idle', tasks: 0, latency: '-', cpu: 8, memory: '234MB' },
            { id: 'growth', name: '自我提高监督员', role: 'GrowthSupervisor', status: 'active', tasks: 2, latency: '67ms', cpu: 12, memory: '345MB' },
            { id: 'investment', name: '复利项目研究员', role: 'InvestmentResearcher', status: 'error', tasks: 0, latency: '-', cpu: 0, memory: '0MB' }
        ];
        
        const mockTasks = [
            { id: 'task_001', name: '生成小红书内容', agent: 'content', status: 'running', progress: 65, startTime: '10:23:45', eta: '2min' },
            { id: 'task_002', name: '检索历史记忆', agent: 'memory', status: 'completed', progress: 100, startTime: '10:20:12', endTime: '10:20:15' },
            { id: 'task_003', name: '代码审查', agent: 'tech', status: 'running', progress: 34, startTime: '10:25:01', eta: '5min' },
            { id: 'task_004', name: '质量检查', agent: 'quality', status: 'pending', progress: 0, startTime: '-', eta: '-' },
            { id: 'task_005', name: '日程同步', agent: 'life', status: 'completed', progress: 100, startTime: '10:15:30', endTime: '10:15:32' }
        ];
        
        const mockMCPs = [
            { name: 'Tavily Search', category: '搜索', status: 'connected', calls: 1234, latency: '234ms' },
            { name: 'Unsplash', category: '内容', status: 'connected', calls: 567, latency: '145ms' },
            { name: 'Supabase', category: '数据', status: 'connected', calls: 3456, latency: '23ms' },
            { name: 'Firecrawl', category: '内容', status: 'error', calls: 0, latency: '-' },
            { name: 'Telegram', category: '社媒', status: 'connected', calls: 89, latency: '456ms' },
            { name: 'Linear', category: '开发', status: 'idle', calls: 0, latency: '-' }
        ];
        
        const mockLogs = [
            { time: '10:30:45', level: 'info', agent: 'supervisor', message: '任务分解完成，分配3个子任务' },
            { time: '10:30:42', level: 'success', agent: 'memory', message: '检索到12条相关记忆片段' },
            { time: '10:30:38', level: 'warning', agent: 'content', message: 'API限流，启用退避策略' },
            { time: '10:30:35', level: 'info', agent: 'tech', message: 'MCP工具调用: Tavily Search' },
            { time: '10:30:30', level: 'error', agent: 'investment', message: '连接超时，无法获取市场数据' },
            { time: '10:30:28', level: 'info', agent: 'supervisor', message: '接收到新任务: 分析Q1财报' }
        ];
        
        // 图标组件
        const Icons = {
            Activity: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>,
            Cpu: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" /></svg>,
            Database: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" /></svg>,
            Terminal: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>,
            Settings: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>,
            Play: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>,
            Pause: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>,
            Refresh: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>,
            Alert: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>,
            Check: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>,
            Zap: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>,
            Layout: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>,
            Tool: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>,
            Brain: () => <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>
        };
        
        // 状态徽章组件
        const StatusBadge = ({ status }) => {
            const styles = {
                active: 'bg-green-500/20 text-green-400 border-green-500/30',
                idle: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
                error: 'bg-red-500/20 text-red-400 border-red-500/30',
                offline: 'bg-gray-500/20 text-gray-400 border-gray-500/30',
                pending: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
                running: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
                completed: 'bg-green-500/20 text-green-400 border-green-500/30',
                connected: 'bg-green-500/20 text-green-400 border-green-500/30'
            };
            
            return (
                <span className={`px-2 py-1 rounded text-xs font-mono border ${styles[status] || styles.offline}`}>
                    {status.toUpperCase()}
                </span>
            );
        };
        
        // 导航栏组件
        const Sidebar = ({ activeTab, setActiveTab }) => {
            const menuItems = [
                { id: 'dashboard', label: '指挥面板', icon: Icons.Layout },
                { id: 'agents', label: 'Agent管理', icon: Icons.Cpu },
                { id: 'workflow', label: '工作流编排', icon: Icons.Activity },
                { id: 'memory', label: '记忆浏览器', icon: Icons.Database },
                { id: 'mcp', label: 'MCP工具', icon: Icons.Tool },
                { id: 'logs', label: '系统日志', icon: Icons.Terminal },
                { id: 'settings', label: '设置', icon: Icons.Settings }
            ];
            
            return (
                <div className="w-64 h-screen glass-card fixed left-0 top-0 z-50 flex flex-col">
                    <div className="p-6 border-b border-cyan-500/20">
                        <h1 className="text-2xl font-bold text-cyan-400 glow-text font-mono">OpenClaw</h1>
                        <p className="text-xs text-gray-400 mt-1">Mission Control v2.0</p>
                    </div>
                    
                    <nav className="flex-1 p-4 space-y-2">
                        {menuItems.map(item => (
                            <button
                                key={item.id}
                                onClick={() => setActiveTab(item.id)}
                                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                                    activeTab === item.id 
                                        ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' 
                                        : 'text-gray-400 hover:bg-white/5 hover:text-white'
                                }`}
                            >
                                <item.icon />
                                <span className="font-medium">{item.label}</span>
                            </button>
                        ))}
                    </nav>
                    
                    <div className="p-4 border-t border-cyan-500/20">
                        <div className="flex items-center gap-3 text-sm text-gray-400">
                            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                            <span>系统运行正常</span>
                        </div>
                        <div className="mt-2 text-xs text-gray-500 font-mono">
                            Uptime: 99.9%
                        </div>
                    </div>
                </div>
            );
        };
        
        // 概览卡片组件
        const StatCard = ({ title, value, subtitle, trend, icon: Icon, color }) => (
            <div className="glass-card p-6 animate-fade-in">
                <div className="flex items-start justify-between">
                    <div>
                        <p className="text-gray-400 text-sm">{title}</p>
                        <h3 className="text-3xl font-bold text-white mt-2 font-mono">{value}</h3>
                        <p className="text-sm mt-1 text-gray-500">{subtitle}</p>
                    </div>
                    <div className={`p-3 rounded-lg bg-${color}-500/20`}>
                        <Icon className={`w-6 h-6 text-${color}-400`} />
                    </div>
                </div>
                {trend && (
                    <div className="mt-4 flex items-center gap-2">
                        <span className={`text-sm ${trend > 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}%
                        </span>
                        <span className="text-xs text-gray-500">vs 上周</span>
                    </div>
                )}
            </div>
        );
        
        // Agent状态卡片
        const AgentCard = ({ agent }) => (
            <div className="glass-card p-4 hover:border-cyan-500/40 transition-all cursor-pointer group">
                <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                        <div className={`w-3 h-3 rounded-full status-${agent.status}`}></div>
                        <div>
                            <h4 className="font-semibold text-white group-hover:text-cyan-400 transition-colors">
                                {agent.name}
                            </h4>
                            <p className="text-xs text-gray-500 font-mono">{agent.role}</p>
                        </div>
                    </div>
                    <StatusBadge status={agent.status} />
                </div>
                
                <div className="grid grid-cols-2 gap-4 mt-4 text-sm">
                    <div>
                        <p className="text-gray-500 text-xs">活跃任务</p>
                        <p className="text-white font-mono">{agent.tasks}</p>
                    </div>
                    <div>
                        <p className="text-gray-500 text-xs">延迟</p>
                        <p className="text-white font-mono">{agent.latency}</p>
                    </div>
                    <div>
                        <p className="text-gray-500 text-xs">CPU</p>
                        <div className="flex items-center gap-2">
                            <div className="w-16 h-1.5 bg-gray-700 rounded-full overflow-hidden">
                                <div 
                                    className="h-full bg-cyan-500 rounded-full"
                                    style={{ width: `${agent.cpu}%` }}
                                ></div>
                            </div>
                            <span className="text-white font-mono">{agent.cpu}%</span>
                        </div>
                    </div>
                    <div>
                        <p className="text-gray-500 text-xs">内存</p>
                        <p className="text-white font-mono">{agent.memory}</p>
                    </div>
                </div>
            </div>
        );
        
        // 任务列表组件
        const TaskList = ({ tasks }) => (
            <div className="glass-card overflow-hidden">
                <div className="p-4 border-b border-cyan-500/20 flex items-center justify-between">
                    <h3 className="font-semibold text-white flex items-center gap-2">
                        <Icons.Activity />
                        活跃任务
                    </h3>
                    <span className="text-xs text-gray-500">{tasks.filter(t => t.status === 'running').length} 运行中</span>
                </div>
                <div className="divide-y divide-cyan-500/10">
                    {tasks.map(task => (
                        <div key={task.id} className="p-4 hover:bg-white/5 transition-colors">
                            <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-3">
                                    <span className="text-cyan-400 font-mono text-sm">#{task.id}</span>
                                    <span className="text-white">{task.name}</span>
                                </div>
                                <StatusBadge status={task.status} />
                            </div>
                            <div className="flex items-center gap-4 text-xs text-gray-500">
                                <span>Agent: {task.agent}</span>
                                <span>开始: {task.startTime}</span>
                                {task.eta && <span>预计: {task.eta}</span>}
                            </div>
                            {task.status === 'running' && (
                                <div className="mt-3">
                                    <div className="flex justify-between text-xs mb-1">
                                        <span className="text-gray-400">进度</span>
                                        <span className="text-cyan-400">{task.progress}%</span>
                                    </div>
                                    <div className="w-full h-1 bg-gray-700 rounded-full overflow-hidden">
                                        <div 
                                            className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full transition-all duration-500"
                                            style={{ width: `${task.progress}%` }}
                                        ></div>
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        );
        
        // 工作流可视化组件
        const WorkflowVisualizer = () => {
            const canvasRef = useRef(null);
            const [nodes, setNodes] = useState([
                { id: 'start', x: 50, y: 200, label: '开始', type: 'start' },
                { id: 'supervisor', x: 250, y: 200, label: '总调度员', type: 'process' },
                { id: 'memory', x: 450, y: 100, label: '记忆检索', type: 'process' },
                { id: 'content', x: 450, y: 300, label: '内容生成', type: 'process' },
                { id: 'quality', x: 650, y: 200, label: '质量检查', type: 'process' },
                { id: 'end', x: 850, y: 200, label: '完成', type: 'end' }
            ]);
            const [connections] = useState([
                { from: 'start', to: 'supervisor', active: true },
                { from: 'supervisor', to: 'memory', active: true },
                { from: 'supervisor', to: 'content', active: true },
                { from: 'memory', to: 'quality', active: false },
                { from: 'content', to: 'quality', active: false },
                { from: 'quality', to: 'end', active: false }
            ]);
            
            useEffect(() => {
                const canvas = canvasRef.current;
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                
                const draw = () => {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    
                    // 绘制连接线
                    connections.forEach(conn => {
                        const fromNode = nodes.find(n => n.id === conn.from);
                        const toNode = nodes.find(n => n.id === conn.to);
                        if (fromNode && toNode) {
                            ctx.beginPath();
                            ctx.moveTo(fromNode.x + 70, fromNode.y + 25);
                            ctx.lineTo(toNode.x, toNode.y + 25);
                            ctx.strokeStyle = conn.active ? '#00D4FF' : '#0066FF';
                            ctx.lineWidth = conn.active ? 3 : 2;
                            ctx.setLineDash(conn.active ? [5, 5] : []);
                            ctx.stroke();
                            
                            // 箭头
                            const angle = Math.atan2(toNode.y - fromNode.y, toNode.x - fromNode.x);
                            ctx.beginPath();
                            ctx.moveTo(toNode.x, toNode.y + 25);
                            ctx.lineTo(
                                toNode.x - 10 * Math.cos(angle - Math.PI / 6),
                                toNode.y + 25 - 10 * Math.sin(angle - Math.PI / 6)
                            );
                            ctx.lineTo(
                                toNode.x - 10 * Math.cos(angle + Math.PI / 6),
                                toNode.y + 25 - 10 * Math.sin(angle + Math.PI / 6)
                            );
                            ctx.fillStyle = conn.active ? '#00D4FF' : '#0066FF';
                            ctx.fill();
                        }
                    });
                };
                
                draw();
            }, [nodes, connections]);
            
            return (
                <div className="glass-card p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="font-semibold text-white flex items-center gap-2">
                            <Icons.Activity />
                            工作流可视化
                        </h3>
                        <div className="flex gap-2">
                            <button className="px-3 py-1 bg-cyan-500/20 text-cyan-400 rounded text-sm border border-cyan-500/30 hover:bg-cyan-500/30">
                                运行
                            </button>
                            <button className="px-3 py-1 bg-gray-700 text-gray-300 rounded text-sm hover:bg-gray-600">
                                暂停
                            </button>
                        </div>
                    </div>
                    
                    <div className="relative h-96 bg-black/30 rounded-lg overflow-hidden">
                        <canvas 
                            ref={canvasRef} 
                            width={1000} 
                            height={400}
                            className="absolute inset-0"
                        />
                        {nodes.map(node => (
                            <div
                                key={node.id}
                                className={`absolute w-32 p-3 rounded-lg border-2 text-center cursor-move transition-all hover:scale-105 ${
                                    node.type === 'start' ? 'border-green-500 bg-green-500/20' :
                                    node.type === 'end' ? 'border-red-500 bg-red-500/20' :
                                    'border-cyan-500 bg-cyan-500/20'
                                }`}
                                style={{ left: node.x, top: node.y }}
                            >
                                <p className="text-white text-sm font-medium">{node.label}</p>
                            </div>
                        ))}
                    </div>
                    
                    <div className="mt-4 flex gap-4 text-xs text-gray-400">
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-green-500"></div>
                            <span>开始节点</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-cyan-500"></div>
                            <span>处理节点</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-red-500"></div>
                            <span>结束节点</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-8 h-0.5 bg-cyan-400"></div>
                            <span>活跃流</span>
                        </div>
                    </div>
                </div>
            );
        };
        
        // 记忆浏览器组件
        const MemoryBrowser = () => {
            const [searchQuery, setSearchQuery] = useState('');
            const [memories] = useState([
                { id: 1, type: 'fact', content: '用户偏好使用小红书平台', confidence: 0.95, timestamp: '2026-02-28' },
                { id: 2, type: 'episode', content: '成功完成Q1财报分析任务', confidence: 0.88, timestamp: '2026-02-27' },
                { id: 3, type: 'semantic', content: 'Python数据分析最佳实践', confidence: 0.92, timestamp: '2026-02-25' },
                { id: 4, type: 'fact', content: '用户工作时间为9:00-18:00', confidence: 0.98, timestamp: '2026-02-20' }
            ]);
            
            return (
                <div className="glass-card p-6">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="font-semibold text-white flex items-center gap-2">
                            <Icons.Brain />
                            记忆浏览器
                        </h3>
                        <div className="flex gap-2">
                            <input
                                type="text"
                                placeholder="搜索记忆..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="px-4 py-2 bg-black/30 border border-cyan-500/30 rounded-lg text-white text-sm focus:outline-none focus:border-cyan-500"
                            />
                            <button className="px-4 py-2 bg-cyan-500/20 text-cyan-400 rounded-lg border border-cyan-500/30 hover:bg-cyan-500/30">
                                搜索
                            </button>
                        </div>
                    </div>
                    
                    <div className="space-y-3">
                        {memories.map(memory => (
                            <div key={memory.id} className="p-4 bg-black/20 rounded-lg border border-cyan-500/10 hover:border-cyan-500/30 transition-all">
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-2">
                                            <span className={`px-2 py-0.5 rounded text-xs ${
                                                memory.type === 'fact' ? 'bg-blue-500/20 text-blue-400' :
                                                memory.type === 'episode' ? 'bg-purple-500/20 text-purple-400' :
                                                'bg-green-500/20 text-green-400'
                                            }`}>
                                                {memory.type}
                                            </span>
                                            <span className="text-xs text-gray-500">{memory.timestamp}</span>
                                        </div>
                                        <p className="text-white">{memory.content}</p>
                                    </div>
                                    <div className="text-right ml-4">
                                        <div className="text-2xl font-bold text-cyan-400 font-mono">
                                            {(memory.confidence * 100).toFixed(0)}%
                                        </div>
                                        <p className="text-xs text-gray-500">置信度</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            );
        };
        
        // MCP工具管理组件
        const MCPManager = () => (
            <div className="glass-card p-6">
                <div className="flex items-center justify-between mb-6">
                    <h3 className="font-semibold text-white flex items-center gap-2">
                        <Icons.Tool />
                        MCP工具状态
                    </h3>
                    <button className="px-4 py-2 bg-cyan-500/20 text-cyan-400 rounded-lg border border-cyan-500/30 hover:bg-cyan-500/30 text-sm">
                        + 添加工具
                    </button>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {mockMCPs.map((mcp, idx) => (
                        <div key={idx} className="p-4 bg-black/20 rounded-lg border border-cyan-500/10 hover:border-cyan-500/30 transition-all">
                            <div className="flex items-start justify-between mb-3">
                                <div>
                                    <h4 className="text-white font-medium">{mcp.name}</h4>
                                    <p className="text-xs text-gray-500">{mcp.category}</p>
                                </div>
                                <StatusBadge status={mcp.status} />
                            </div>
                            <div className="grid grid-cols-2 gap-4 text-sm">
                                <div>
                                    <p className="text-gray-500 text-xs">调用次数</p>
                                    <p className="text-white font-mono">{mcp.calls.toLocaleString()}</p>
                                </div>
                                <div>
                                    <p className="text-gray-500 text-xs">延迟</p>
                                    <p className="text-white font-mono">{mcp.latency}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        );
        
        // 日志终端组件
        const LogTerminal = () => (
            <div className="glass-card overflow-hidden">
                <div className="p-4 border-b border-cyan-500/20 flex items-center justify-between">
                    <h3 className="font-semibold text-white flex items-center gap-2">
                        <Icons.Terminal />
                        系统日志
                    </h3>
                    <div className="flex gap-2">
                        <button className="p-2 hover:bg-white/10 rounded">
                            <Icons.Refresh className="w-4 h-4" />
                        </button>
                        <button className="p-2 hover:bg-white/10 rounded">
                            <Icons.Settings className="w-4 h-4" />
                        </button>
                    </div>
                </div>
                <div className="terminal p-4 h-64 overflow-y-auto font-mono text-sm">
                    {mockLogs.map((log, idx) => (
                        <div key={idx} className="terminal-line mb-1">
                            <span className="text-gray-500">[{log.time}]</span>
                            <span className={`mx-2 ${
                                log.level === 'error' ? 'text-red-400' :
                                log.level === 'warning' ? 'text-yellow-400' :
                                log.level === 'success' ? 'text-green-400' :
                                'text-cyan-400'
                            }`}>
                                [{log.level.toUpperCase()}]
                            </span>
                            <span className="text-purple-400">{log.agent}</span>
                            <span className="text-gray-300 ml-2">{log.message}</span>
                        </div>
                    ))}
                </div>
            </div>
        );
        
        // 主仪表板视图
        const DashboardView = () => (
            <div className="space-y-6 animate-fade-in">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <StatCard 
                        title="活跃Agent" 
                        value="6/8" 
                        subtitle="2个离线" 
                        trend={12} 
                        icon={Icons.Cpu} 
                        color="cyan"
                    />
                    <StatCard 
                        title="今日任务" 
                        value="47" 
                        subtitle="成功率 94%" 
                        trend={8} 
                        icon={Icons.Activity} 
                        color="green"
                    />
                    <StatCard 
                        title="Token消耗" 
                        value="2.4M" 
                        subtitle="成本 $12.5" 
                        trend={-5} 
                        icon={Icons.Zap} 
                        color="yellow"
                    />
                    <StatCard 
                        title="记忆检索" 
                        value="1,234" 
                        subtitle="命中率 89%" 
                        trend={15} 
                        icon={Icons.Database} 
                        color="purple"
                    />
                </div>
                
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2">
                        <TaskList tasks={mockTasks} />
                    </div>
                    <div>
                        <LogTerminal />
                    </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {mockAgents.slice(0, 4).map(agent => (
                        <AgentCard key={agent.id} agent={agent} />
                    ))}
                </div>
            </div>
        );
        
        // Agent管理视图
        const AgentsView = () => (
            <div className="space-y-6 animate-fade-in">
                <div className="flex items-center justify-between">
                    <h2 className="text-2xl font-bold text-white">Agent管理</h2>
                    <button className="px-4 py-2 bg-cyan-500/20 text-cyan-400 rounded-lg border border-cyan-500/30 hover:bg-cyan-500/30">
                        + 部署新Agent
                    </button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {mockAgents.map(agent => (
                        <AgentCard key={agent.id} agent={agent} />
                    ))}
                </div>
            </div>
        );
        
        // 主应用组件
        const App = () => {
            const [activeTab, setActiveTab] = useState('dashboard');
            
            const renderContent = () => {
                switch(activeTab) {
                    case 'dashboard':
                        return <DashboardView />;
                    case 'agents':
                        return <AgentsView />;
                    case 'workflow':
                        return <WorkflowVisualizer />;
                    case 'memory':
                        return <MemoryBrowser />;
                    case 'mcp':
                        return <MCPManager />;
                    case 'logs':
                        return <LogTerminal />;
                    default:
                        return <DashboardView />;
                }
            };
            
            return (
                <div className="flex min-h-screen bg-gray-900">
                    <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
                    <main className="flex-1 ml-64 p-8">
                        <header className="mb-8 flex items-center justify-between">
                            <div>
                                <h1 className="text-3xl font-bold text-white">
                                    {activeTab === 'dashboard' && '指挥面板'}
                                    {activeTab === 'agents' && 'Agent管理'}
                                    {activeTab === 'workflow' && '工作流编排'}
                                    {activeTab === 'memory' && '记忆浏览器'}
                                    {activeTab === 'mcp' && 'MCP工具管理'}
                                    {activeTab === 'logs' && '系统日志'}
                                    {activeTab === 'settings' && '系统设置'}
                                </h1>
                                <p className="text-gray-400 mt-1">
                                    {new Date().toLocaleString('zh-CN', { 
                                        year: 'numeric', 
                                        month: 'long', 
                                        day: 'numeric', 
                                        hour: '2-digit', 
                                        minute: '2-digit' 
                                    })}
                                </p>
                            </div>
                            <div className="flex items-center gap-4">
                                <div className="flex items-center gap-2 px-4 py-2 glass-card">
                                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                                    <span className="text-sm text-gray-300">系统正常</span>
                                </div>
                                <button className="p-2 glass-card hover:bg-white/10 rounded-lg">
                                    <Icons.Alert className="w-5 h-5 text-gray-400" />
                                </button>
                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white font-bold">
                                    A
                                </div>
                            </div>
                        </header>
                        
                        {renderContent()}
                    </main>
                </div>
            );
        };
        
        // 渲染应用
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>'''

# 保存文件
with open('/mnt/kimi/output/openclaw_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dashboard_html)

print("✅ OpenClaw Dashboard 已生成!")
print("📁 文件位置: /mnt/kimi/output/openclaw_dashboard.html")
print("\n🎯 面板特性:")
print("  • 赛博朋克/指挥中心风格设计")
print("  • 实时Agent状态监控 (8个角色)")
print("  • 任务队列与进度追踪")
print("  • 可视化工作流编排器")
print("  • 记忆浏览器 (向量检索)")
print("  • MCP工具管理面板")
print("  • 实时日志终端")
print("  • 响应式布局")
