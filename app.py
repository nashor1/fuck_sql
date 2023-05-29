from flask import Flask, jsonify, request, render_template
import mysql.connector
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

app = Flask(__name__)

# 数据库连接配置
config = {
    'user': 'zxcasdqwea',
    'password': 'ljhawSu11523@#',
    'host': 'rm-0jl2y08crq122079fxo.mysql.rds.aliyuncs.com',
    'database': 'a_-1',
    'raise_on_warnings': True
}





# 定义单个表的查询函数
def query_table(table_name,name,phone):
    try:
        # 创建全局的数据库连接
        cnx = mysql.connector.connect(**config)
        # 创建游标对象
        cursor = cnx.cursor()

        # 执行查询语句
        query = "SELECT * FROM {} WHERE name like '%{}%' "
        if phone != None:
            query += "and Mobile like '%{}%'"
            cursor.execute(query.format(table_name, name, phone))
        else:
            cursor.execute(query.format(table_name, name))

        # 获取查询结果
        results = cursor.fetchall()

        # 关闭游标
        cursor.close()

        return results

    except Exception as e:
        return str(e)


# 定义路由执行多线程查询
@app.route('/query', methods=['GET'])
def query_database():
    try:
        # 获取 name 参数的值
        name = request.args.get('name')
        phone = request.args.get('phone')

        # 使用线程池执行多线程查询
        with ThreadPoolExecutor(max_workers=10) as executor:
            # 创建任务列表
            tasks = []

            # 遍历每个表名
            for table_name in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
                # 提交查询任务给线程池
                task = executor.submit(query_table, table_name, name, phone)
                tasks.append(task)

            results = []
            # 获取所有查询结果
            for future in as_completed(tasks):
                try:
                    result = future.result()  # 获取任务的返回结果
                    results.append(result)
                    print(f"任务返回结果：{result}")
                except Exception as e:
                    print(f"任务执行出错：{e}")

        # 将结果转换为JSON格式并返回
        # return jsonify(results)
        return render_template('sql.html', results=jsonify(results).json)


    #你不要返回一个list去浏览器那里  啥？，返回一个list去浏览器就会unicode编码
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run()
